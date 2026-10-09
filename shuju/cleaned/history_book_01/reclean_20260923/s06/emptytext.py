import json
from pathlib import Path
D=json.loads(Path('shuju/cleaned/history_book_01/reclean_20260923/baseline.json').read_text(encoding='utf-8')); B={x['id']:x for x in D['blocks']}
for k in D['knowledge']:
 if not any(k['id'].startswith(f'history_book_01_p{i:04d}_') for i in range(187,209)):continue
 empties=[x for x,v in [('flow',k.get('flow')),('points',k.get('points')),('background',k.get('background')),('impact',k.get('impact'))] if not v]
 if empties:
  src=' '.join((B[x].get('clean_text') or '') for x in k.get('evidence_block_ids',[]) if x in B)
  sm=(k.get('summary') or {}).get('text','')
  print(k['id'],k['title'],'EMPTY',','.join(empties),'SUM',sm[:160],'SRC',src[:240])
