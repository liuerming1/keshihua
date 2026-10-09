import json,re
from pathlib import Path
d=json.loads(Path('shuju/cleaned/history_book_01/reclean_20260923/baseline.json').read_text(encoding='utf-8')); B={b['id']:b for b in d['blocks']}; Ks=[k for k in d['knowledge'] if any(k['id'].startswith(f'history_book_01_p{i:04d}_') for i in range(187,224))]
pat=re.compile(r'因为|由于|背景|为了|为.*?奠定|促使|推动|促进|影响|使得|从而|因此|标志着|意义|带来|导致|有利于|有助于')
for k in Ks:
 t=' '.join(B[x].get('clean_text') or '' for x in k.get('evidence_block_ids',[]) if x in B)
 if (not k.get('background') or not k.get('impact')) and pat.search(t): print(k['id'],k['title'],'BG=',not bool(k.get('background')),'IM=',not bool(k.get('impact')),'TXT=',t[:450])
