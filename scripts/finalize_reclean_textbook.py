"""Apply reviewed page patches and explicit cross-page decisions with lineage."""
import argparse
import copy
import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from merge_reclean_reviews import merge, WORK, ROOT, read
from audit_reclean_contract import check as check_contract


def unique(values):
    result=[]
    for value in values:
        if value not in result: result.append(value)
    return result


def finalize():
    data,report=merge()
    residual_cleanup=[]
    for block in data['blocks']:
        original_text=block.get('clean_text')
        if not isinstance(original_text,str): continue
        cleaned=original_text
        # Exact remaining lines of the repeatedly observed PDF footer watermark.
        # Remove only these literal fragments, never the surrounding source text.
        for fragment in ('_\x97SæPZNÖu(', 'g*~Ïc\x88gCN'):
            cleaned=cleaned.replace(fragment,'')
        if cleaned!=original_text:
            block['clean_text']=cleaned.strip()
            residual_cleanup.append(block['id'])
    decisions=read(WORK/'primary_decisions.json')
    data['prior_validation']=copy.deepcopy(data.get('validation'))
    data['prior_finalization_report']=copy.deepcopy(data.get('finalization_report'))
    asset_refresh=[]
    image_review_path=WORK/'primary/image_text_review.json'
    if image_review_path.exists():
        reviews=read(image_review_path)
        assets_by_id={a['id']:a for a in data['assets']}
        for reviewed in reviews:
            current=assets_by_id[reviewed['id']]
            if any(current.get(f)!=reviewed.get(f) for f in ('file_path','bbox','export')):
                raise ValueError('Image text review changed exported image: '+reviewed['id'])
            reviewed['prior_notes']=copy.deepcopy(current.get('notes',[]))
            current.update(reviewed)
    for asset in data['assets']:
        if asset.get('file_path') and asset.get('export') and any('未导出' in n for n in asset.get('notes',[])):
            asset.setdefault('prior_notes',copy.deepcopy(asset['notes']))
            refreshed=[]
            for note in asset['notes']:
                if '未导出' in note:
                    prefix=note.split('未导出')[0].rstrip('；;，。 ')
                    note=(prefix+'；' if prefix else '')+'本包已导出独立PNG，路径与哈希见file_path和export。'
                    if asset['type']=='map': note+='历史地图几何仍未地理配准。'
                refreshed.append(note)
            asset['notes']=refreshed
            asset_refresh.append(asset['id'])
    for page in data['pages']:
        partial_images=[a['id'] for a in data['assets'] if a['page_id']==page['id'] and
            a.get('text_review',{}).get('status') in ('partial','unreadable')]
        if partial_images:
            page['image_status']='partial'
            page['notes']=unique(page['notes']+['独立图像可读取；其中小字/影像文字仍有源图清晰度限制：'+','.join(partial_images)])
    by_id={k['id']:k for k in data['knowledge']}
    archives=[]; redirects={}; ledger=[]
    audit_by_id={a['id']:a for a in report['audit']}
    for item in data['knowledge']:
        audit=audit_by_id[item['id']]
        item['reclean_review']={'status':'needs_review' if audit['decision']=='needs_review' else 'agent_reviewed',
                               'checked_fields':audit['checked_fields'],'note':audit['note'],
                               'empty_reasons':audit['empty_reasons']}
        old=copy.deepcopy(item.get('finalization'))
        item['prior_finalization']=old
        item['finalization']=dict(old or {})
        item['finalization']['status']='needs_review' if audit['decision']=='needs_review' else 'qualified'
        item['finalization']['fact_note']='本轮已逐条清洗复核；原事实核验记录保留。'+audit['note']
        item['finalization']['interpretation']='reclean review is evidence-based extraction review, not independent verification of every historical claim'
    def absorb(target,other):
        if other['finalization']['status']=='needs_review':
            target['finalization']['status']='needs_review'
            target['reclean_review']['status']='needs_review'
            target['finalization']['fact_note']+=' 合并来源仍待复核：'+other['id']+'；'+other['reclean_review']['note']
        for field in ('evidence_block_ids','asset_ids','person_ids','source_inventory_ids','themes','uncertainties','place_refs'):
            target[field]=unique(target[field]+other[field])
        target['time']['evidence_block_ids']=unique(target['time']['evidence_block_ids']+other['time']['evidence_block_ids'])
        for field in ('flow','points'):
            target[field]=unique(target[field]+other[field])
        for field in ('background','impact'):
            if target[field] is None and other[field] is not None: target[field]=copy.deepcopy(other[field])
        target.setdefault('source_variants',[]).append({'original_id':other['id'],'title':other['title'],
            'time':other['time'],'summary':other['summary'],'background':other['background'],'impact':other['impact']})
        target.setdefault('merged_from_ids',[]).append(other['id'])
    for group in decisions['merges']:
        canonical=by_id[group['canonical_id']]
        for donor_id in group['duplicate_ids']:
            donor=by_id[donor_id]
            absorb(canonical,donor)
            archives.append(copy.deepcopy(donor));redirects[donor_id]=[canonical['id']]
        ledger.append(group)
    for decision in decisions['redistributions']:
        donor=by_id[decision['source_id']]
        for target_id in decision['target_ids']:
            target=by_id[target_id]
            # Shared overview supplies evidence, not the other event's time or claims.
            for field in ('evidence_block_ids','asset_ids','source_inventory_ids'):
                target[field]=unique(target[field]+donor[field])
            target.setdefault('source_variants',[]).append({'original_id':donor['id'],'title':donor['title'],
                'time':donor['time'],'summary':donor['summary']})
        archives.append(copy.deepcopy(donor));redirects[donor['id']]=decision['target_ids'];ledger.append(decision)
    data['knowledge']=[k for k in data['knowledge'] if k['id'] not in redirects]
    for item in data['knowledge']:
        for field in ('flow','points','background','impact'):
            if item.get(field): item['reclean_review']['empty_reasons'].pop(field,None)
    def mapped(ids):
        return unique([value for key in ids for value in redirects.get(key,[key])])
    for inv in data['inventory']:
        inv['knowledge_ids']=mapped(inv['knowledge_ids'])
    for relation in data['relations']:
        for field in ('from_knowledge_id','to_knowledge_id'):
            if relation[field] in redirects:
                targets=redirects[relation[field]]
                if len(targets)!=1: raise ValueError('Ambiguous redistributed relation requires explicit review')
                relation[field]=targets[0]
    for item in data['knowledge']:
        item['source_inventory_ids']=[i['id'] for i in data['inventory'] if item['id'] in i['knowledge_ids']]
    for issue in data['review_issues']:
        if issue['id'] in decisions.get('resolved_issues',{}):
            issue['prior_finalization_status']=issue.get('finalization_status','open')
            issue['finalization_status']='resolved'
            issue['resolution_note']=decisions['resolved_issues'][issue['id']]
        issue['record_ids']=mapped(issue['record_ids'])
    carry_review={}
    for n in range(1,7):
        for c in read(WORK/f's{n:02}.patch.json').get('carryover_review',[]):
            if c['index'] in carry_review: raise ValueError('Duplicate carryover review')
            carry_review[c['index']]=c
    old_carry=data['batch'].get('carryover',[])
    if set(carry_review)!=set(range(len(old_carry))):
        raise ValueError(f'Missing carryover reviews: {set(range(len(old_carry)))-set(carry_review)}')
    data['batch']['carryover']=[]
    for number,old in enumerate(old_carry):
        result=carry_review[number]
        if result['status']!='resolved':
            data['batch']['carryover'].append({'type':old['type'],'record_ids':mapped(old['record_ids']),
                'description':result['reason'],'next_action':result.get('next_action','核对所列证据的剩余内容，不重新调度已读页。')})
    for n,item in enumerate(report['open_items'],1):
        # A redistributed overview is closed by the explicit canonical mapping above.
        if item.get('record_ids') and all(i in redirects for i in item['record_ids']):
            continue
        data['review_issues'].append({'id':f'history_book_01_reclean_issue_{n:03}',
          'record_ids':mapped(item.get('record_ids',[])),'category':'source','description':item['reason'],
          'evidence_block_ids':item.get('evidence_block_ids',[]),'suggested_action':item['next_action'],
          'blocking':item.get('blocking',False),'status':'open','finalization_status':'open'})
    completed=[];partial=[];unread=[]
    for page in data['pages']:
        states=[page['text_status'],page['image_status']]
        number=page['pdf_page_number']
        if all(s in ('complete','not_applicable') for s in states): completed.append(number)
        elif all(s=='unread' for s in states): unread.append(number)
        else: partial.append(number)
    data['batch'].update(completed_pdf_pages=completed,partial_pdf_pages=partial,unprocessed_pdf_pages=unread,
                         complete=not(partial or unread),next_pdf_page=min(unread) if unread else None,
                         processing_status='unprocessed_pages_remain' if unread else 'complete_with_source_limitations' if partial else 'complete')
    data['knowledge_aliases']=redirects
    data['archived_knowledge_candidates']=archives
    data['reclean_report']={'source_sha256':report['baseline_sha256'],'reviewed_candidate_count':len(report['audit']),
        'canonical_knowledge_count':len(data['knowledge']),'archived_candidate_count':len(archives),
        'primary_footer_fragment_cleanup_ids':residual_cleanup,
        'asset_metadata_refreshed_ids':asset_refresh,
        'image_text_review':[{'id':a['id'],**a['text_review']} for a in data['assets'] if a.get('text_review')],
        'lineage':ledger,'carryover_review':[carry_review[i] for i in range(len(old_carry))],
        'open_items':[i for i in report['open_items'] if not (i.get('record_ids') and all(r in redirects for r in i['record_ids']))],
        'status':'cleaned_with_explicit_qualifications',
        'semantic_boundary':'逐条源证据清洗；未宣称所有史实与图片小字完成独立人工审核或历史地图地理配准。'}
    data['finalization_report']['knowledge_count']=len(data['knowledge'])
    data['finalization_report']['fact_status_counts']=dict(Counter(k['finalization']['status'] for k in data['knowledge']))
    data['finalization_report']['issue_status_counts']=dict(Counter(i.get('finalization_status','open') for i in data['review_issues']))
    data['finalization_report']['import_status']='recleaned_with_qualifications_geometry_pending'
    violations=check_contract(data)
    if violations: raise ValueError(json.dumps(violations,ensure_ascii=False))
    data['validation']={'structure_check_status':'pending_final_validation',
        'duplicate_ids':[],'dangling_references':[],'page_coverage_issues':[],'time_issues':[],
        'source_issues':data['reclean_report']['open_items'],
        'semantic_review_status':'source_extraction_reviewed_with_qualifications',
        'semantic_review_scope':'六段逐条提取审阅及主代理重点复核，不等同于每项史实的独立外部考证。',
        'contract_findings':[],
        'unreadable_blocks':[b['id'] for b in data['blocks'] if '[无法辨认]' in (b.get('clean_text') or '')],
        'unprocessed_assets':[]}
    return data,report


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=WORK/'all_recleaned.json')
    parser.add_argument('--publish',action='store_true')
    args=parser.parse_args()
    previous_output_hash=None
    if args.output.exists():
        previous=read(args.output)
        if previous.get('reclean_report',{}).get('source_sha256')==hashlib.sha256((WORK/'baseline.json').read_bytes()).hexdigest():
            previous_output_hash=hashlib.sha256(args.output.read_bytes()).hexdigest()
    data,report=finalize()
    args.output.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    from validate_pdf_cleaning import check as check_schema
    _, schema_issues=check_schema(args.output)
    if schema_issues:
        raise ValueError(json.dumps(schema_issues,ensure_ascii=False))
    subprocess.run([sys.executable,'-B','-X','utf8',str(ROOT/'scripts/validate_textbook_package.py'),
        '--package',str(args.output),'--public-dir',str(ROOT/'public')],check=True)
    data['validation']['structure_check_status']='passed'
    data['validation']['asset_hash_check_status']='passed'
    args.output.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    (WORK/'merge_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    if args.publish:
        target=ROOT/'public/data/history_book_01.json'
        current=hashlib.sha256(target.read_bytes()).hexdigest()
        output_hash=hashlib.sha256(args.output.read_bytes()).hexdigest()
        if current not in (report['baseline_sha256'],output_hash,previous_output_hash):
            raise ValueError('Published file changed outside this review; refusing overwrite')
        pending=target.with_suffix('.json.pending')
        pending.write_bytes(args.output.read_bytes())
        pending.replace(target)
    print(f'Cleaned {len(data["knowledge"])} canonical records; {len(data["archived_knowledge_candidates"])} originals preserved')
