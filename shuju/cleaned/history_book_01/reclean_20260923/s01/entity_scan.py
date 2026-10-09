import json
from pathlib import Path
D=json.loads(Path('shuju/cleaned/history_book_01/reclean_20260923/baseline.json').read_text(encoding='utf8'))
for k in D['knowledge']:
 if 9 <= int(k['id'].split('_p')[1].split('_')[0]) <= 38:
  if k.get('person_ids') or k.get('place_refs'):
   print(k['id'],k['title'],'persons',[(x, next((p['name_as_written'] for p in D['people'] if p['id']==x),'')) for x in k.get('person_ids',[])],'places',[(x['place_id'], next((p['name_as_written'] for p in D['places'] if p['id']==x['place_id']),''),x['role']) for x in k.get('place_refs',[])])
print('\nALL people pages 19-20')
for p in D['people']:
 if any(e.startswith(('history_book_01_p0019','history_book_01_p0020')) for e in p['evidence_block_ids']): print(p)
