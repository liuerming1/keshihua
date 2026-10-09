import json
from pathlib import Path
root=Path('shuju/cleaned/history_book_01/reclean_20260923')
p=json.loads((root/'s01.patch.json').read_text(encoding='utf-8'))
d=json.loads((root/'baseline.json').read_text(encoding='utf-8'))
out={k:list(v) if isinstance(v,list) else v for k,v in d.items()}
for name,updates in p['updates'].items():
 if name not in out or not isinstance(out[name],list):continue
 baseline=out[name]; current={x.get('id'):x for x in baseline};
 for record in updates: current[record.get('id')]=record
 out[name]=list(current.values())
# This combined audit fixture is only for content-field checks; parent merge owns batch carryover replacement.
out['batch']=dict(out['batch']);out['batch']['complete']=False
(root/'s01'/'audit_package.json').write_text(json.dumps(out,ensure_ascii=False),encoding='utf-8')
