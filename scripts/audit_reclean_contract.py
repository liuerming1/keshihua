"""Read-only semantic-contract checks beyond JSON shape; not historical verification."""
import argparse
import json
import re
from pathlib import Path


def check(data):
    findings = []
    def add(code, record, detail):
        findings.append({'code': code, 'record_id': record, 'detail': detail})
    for item in data['knowledge']:
        t = item['time']
        if t['mode'] == 'point' and t['start_year'] is None:
            add('point_without_year', item['id'], '单点事件没有明确年份，应拆分或改为不确定时间。')
        if t['mode'] == 'unknown' and any(t[f] is not None for f in ('start_year', 'end_year', 'earliest_year', 'latest_year')):
            add('unknown_with_year', item['id'], '未知时间模式与已有数值年份冲突，应按来源重新判断。')
        if '距今' in (t.get('source_text') or '') and not t.get('reference_epoch') and any(t[f] is not None for f in ('start_year', 'end_year', 'earliest_year', 'latest_year')):
            add('relative_date_without_epoch',item['id'],'距今年代缺少换算历元，不能直接当作公历负年份。')
        for lo, hi in (('start_year', 'end_year'), ('earliest_year', 'latest_year')):
            if t[lo] is not None and t[hi] is not None and t[lo] > t[hi]:
                add('reversed_time', item['id'], f'{lo}晚于{hi}。')
        if t['end_status'] == 'known' and t['end_year'] is None:
            add('known_end_missing', item['id'], '结束状态为已知，但缺少结束年。')
        for field in ('summary', 'background', 'impact', 'flow', 'points'):
            value = item[field]
            claims = value if isinstance(value, list) else [value] if value else []
            for claim in claims:
                if not claim.get('text', '').strip() or not (claim.get('evidence_block_ids') or claim.get('external_source_ids')):
                    add('claim_without_evidence', item['id'], field)
    for block in data['blocks']:
        text = block.get('clean_text') or ''
        if re.search(r'NÅO|\x00|\ufffd|[\x80-\x9f]', text):
            add('unclean_encoding', block['id'], 'clean_text仍有已知编码异常，需要对原页处理。')
        if re.search(r'[（(][^）)\n]*[a-z][A-Z][^）)\n]*[）)]',text):
            add('possible_pinyin_encoding',block['id'],'括号内有混合大小写的可疑拼音编码，需回看原页读音。')
        if re.search(r'已按视觉顺序整理|目录正文不在本批', text):
            add('process_note_as_text', block['id'], '操作说明替代了清洗原文。')
    for carry in data['batch'].get('carryover', []):
        if data['batch'].get('complete') and re.search(r'下一批从|后续批次从|从PDF页序\d+继续', carry.get('next_action', '')):
            add('stale_continuation', ','.join(carry.get('record_ids', [])), carry['next_action'])
    return findings

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('package', type=Path)
    args = parser.parse_args()
    data = json.loads(args.package.read_text(encoding='utf-8-sig'))
    findings = check(data)
    print(json.dumps({'kind':'contract_check_not_fact_review','findings':findings,'count':len(findings)},ensure_ascii=False,indent=2))
    raise SystemExit(1 if findings else 0)
