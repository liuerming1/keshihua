import json,difflib
from pathlib import Path
W=Path('shuju/cleaned/history_book_01/reclean_20260923');b=json.loads((W/'baseline.json').read_text(encoding='utf-8'));bi={x['id']:x for x in b['blocks']}
for sl in ['s04','s05']:
 p=json.loads((W/f'{sl}.patch.json').read_text(encoding='utf-8'));print('\n###',sl)
 for x in p['updates']['blocks']:
  o=bi[x['id']]['clean_text'] or ''; n=x['clean_text'] or ''
  if o==n:continue
  print('\n',x['id'],'length',len(o),'->',len(n),'raw same',x.get('raw_text')==bi[x['id']].get('raw_text'))
  sm=difflib.SequenceMatcher(a=o,b=n,autojunk=False); parts=[]
  for tag,i,j,k,l in sm.get_opcodes():
   if tag!='equal':parts.append(f'{tag.upper()} old={o[i:j]!r} new={n[k:l]!r}')
  print('\n'.join(parts)[:1200])
