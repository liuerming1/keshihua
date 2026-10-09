import json,pathlib
r=pathlib.Path('shuju/cleaned/history_book_01/reclean_20260923'); p=json.loads((r/'s05.patch.json').read_text(encoding='utf-8')); b=json.loads((r/'baseline.json').read_text(encoding='utf-8'))
for kid in ['history_book_01_p0150_k001','history_book_01_p0150_k002']:
 x=next(x for x in p['updates']['knowledge'] if x['id']==kid); print(json.dumps(x,ensure_ascii=False,indent=2))
print('corrupt count',sum(1 for z in b['blocks'] if 150<=int(z['page_id'].split('_p')[1])<=186 and 'NÅO' in (z.get('clean_text') or '')))
