import json,re
from pathlib import Path
D=json.loads(Path('shuju/cleaned/history_book_01/reclean_20260923/baseline.json').read_text(encoding='utf8')); B={b['id']:b for b in D['blocks']}
def pg(k):
 m=re.search(r'_p(\d{4})_',k['id']);return int(m.group(1)) if m else 999
for k in D['knowledge']:
 p=pg(k)
 if 8<=p<=38:
  print(f"{p:02} {k['id']} {k['title']} | time={k['time']['source_text']} ({k['time']['mode']} {k['time']['start_year']},{k['time']['end_year']} {k['time']['end_status']}) | s={bool(k['summary'])} fl={len(k['flow'])} pt={len(k['points'])} bg={bool(k['background'])} im={bool(k['impact'])} refs={len(k['place_refs'])} pers={len(k['person_ids'])}")
  if k.get('points'): print(' pts:',' / '.join(x['text'] for x in k['points']))
