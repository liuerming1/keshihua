import json
from pathlib import Path
d=json.loads(Path('shuju/cleaned/history_book_01/reclean_20260923/baseline.json').read_text(encoding='utf-8'))
ks=[k for k in d['knowledge'] if any(k['id'].startswith(f'history_book_01_p{i:04d}_') for i in range(187,224))]
for k in ks:
 p=k['id'].split('_p')[1][:4]
 if int(p)>=197 and int(p)<=221:
  print(k['id'],k['title'],'| time=',k['time'].get('source_text'),'| s=',(k.get('summary') or {}).get('text','')[:110], '| f',len(k.get('flow',[])),'p',len(k.get('points',[])),'b',bool(k.get('background')),'i',bool(k.get('impact')),'| persons',k.get('person_ids'))
