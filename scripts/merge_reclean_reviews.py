"""Merge six page-owned review patches without changing the published package."""
import argparse
import copy
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / 'shuju/cleaned/history_book_01/reclean_20260923'
RANGES = [(1,38),(39,75),(76,112),(113,149),(150,186),(187,223)]
COLLECTIONS = ('knowledge','blocks','pages','assets','relations','review_issues','places')

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def merge():
    source=WORK/'baseline.json'
    digest=hashlib.sha256(source.read_bytes()).hexdigest()
    original=read(source)
    data=copy.deepcopy(original)
    pages={p['id']:p['pdf_page_number'] for p in data['pages']}
    blocks={b['id']:b for b in data['blocks']}
    approved={(a['slice'],a['collection'],a['id']):a for a in read(WORK/'primary_decisions.json').get('approved_additions',[])}
    for (slice_id,collection,record_id), approval in approved.items():
        if collection not in ('blocks','places') or any(r['id']==record_id for r in original[collection]):
            raise ValueError(f'Invalid approved addition: {record_id}')
        records=read(WORK/f'{slice_id}.patch.json')['updates'][collection]
        added=next(r for r in records if r['id']==record_id)
        payload=added['raw_text'] if collection=='blocks' else json.dumps(added,ensure_ascii=False,sort_keys=True)
        expected_hash=approval.get('raw_text_sha256') if collection=='blocks' else approval['record_sha256']
        if hashlib.sha256(payload.encode()).hexdigest()!=expected_hash:
            raise ValueError(f'Approved source text changed: {record_id}')
        if collection=='blocks': blocks[record_id]=added
    def owner(record):
        match=re.search(r'_p(\d{4})', record['id'])
        if match:
            return int(match[1])
        if record.get('page_id'):
            return pages[record['page_id']]
        refs=record.get('evidence_block_ids',[])
        return min((pages[blocks[b]['page_id']] for b in refs if b in blocks), default=None)
    index={name:{r['id']:i for i,r in enumerate(data[name])} for name in COLLECTIONS}
    audit=[]; changes=[]; proposals=[]; open_items=[]; seen=set()
    for number,(first,last) in enumerate(RANGES,1):
        name=f's{number:02}'
        patch=read(WORK/f'{name}.patch.json')
        if patch['slice']!=name or patch['page_range']!=[first,last] or patch['baseline_sha256'].lower()!=digest:
            raise ValueError(f'{name}: identity/range/baseline mismatch')
        expected={k['id'] for k in original['knowledge'] if first<=owner(k)<=last}
        actual=[a['id'] for a in patch['knowledge_audit']]
        if set(actual)!=expected or len(actual)!=len(expected):
            raise ValueError(f'{name}: incomplete/duplicate per-knowledge review; missing={expected-set(actual)}')
        for item in patch['knowledge_audit']:
            if set(item['checked_fields'])!={'time','summary','flow','points','background','impact','references'}:
                raise ValueError(f'{name}: incomplete checked fields: {item["id"]}')
            if item['decision'] not in ('changed','retained','needs_review') or not item.get('note','').strip():
                raise ValueError(f'{name}: invalid review decision or missing explanation: {item["id"]}')
            if not set(item['evidence_block_ids']) <= blocks.keys():
                raise ValueError(f'{name}: review cites nonexistent evidence: {item["id"]}')
            updated=next((r for r in patch['updates'].get('knowledge',[]) if r['id']==item['id']),None)
            if updated and updated.get('reclean_review',{}).get('status')=='needs_review' and item['decision']!='needs_review':
                raise ValueError(f'{name}: unresolved review incorrectly marked complete: {item["id"]}')
            effective=updated or original['knowledge'][index['knowledge'][item['id']]]
            for field in ('flow','points','background','impact'):
                if not effective.get(field) and not item.get('empty_reasons',{}).get(field,'').strip():
                    raise ValueError(f'{name}: missing reason for empty {field}: {item["id"]}')
        audit.extend(patch['knowledge_audit'])
        for collection, records in patch['updates'].items():
            if collection not in COLLECTIONS:
                raise ValueError(f'{name}: unsupported collection {collection}')
            for record in records:
                key=(collection,record['id'])
                if key in seen:
                    raise ValueError(f'Conflicting patch {key}')
                seen.add(key)
                if record['id'] not in index[collection]:
                    if ((name,collection,record['id']) not in approved and collection!='review_issues') or owner(record) is None or not first<=owner(record)<=last:
                        raise ValueError(f'{name}: additions require explicit primary approval: {key}')
                    index[collection][record['id']]=len(data[collection])
                    data[collection].append(record)
                    changes.append({'slice':name,'collection':collection,'id':record['id'],'fields':['added']})
                    continue
                current=data[collection][index[collection][record['id']]]
                page=owner(current)
                if page is None or not first<=page<=last:
                    raise ValueError(f'{name}: record outside page ownership: {key} ({page})')
                if collection=='blocks' and current['raw_text']!=record['raw_text']:
                    raise ValueError(f'{name}: raw_text is immutable: {key}')
                if collection=='assets' and any(current.get(f)!=record.get(f) for f in ('file_path','bbox','export')):
                    raise ValueError(f'{name}: image export changed without export verification: {key}')
                data[collection][index[collection][record['id']]]=record
                changes.append({'slice':name,'collection':collection,'id':record['id'],'fields':sorted(f for f in set(current)|set(record) if current.get(f)!=record.get(f))})
        proposals.append({'slice':name,'splits':patch.get('split_proposals',[]),'merges':patch.get('merge_proposals',[])})
        open_items.extend(patch.get('open_items',[]))
    if len(audit)!=len(original['knowledge']):
        raise ValueError('Global review coverage mismatch')
    report={'baseline_sha256':digest,'reviewed_knowledge_count':len(audit),'updated_records':len(changes),'changes':changes,'audit':audit,'proposals':proposals,'open_items':open_items,'status':'assembled_pending_primary_review'}
    return data,report

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=WORK/'assembled.json')
    args=parser.parse_args()
    data,report=merge()
    args.output.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (WORK/'merge_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Assembled {len(data["knowledge"])} records; {report["updated_records"]} updated, primary review still required')
