import json,copy
from pathlib import Path
R=Path('shuju/cleaned/history_book_01/reclean_20260923')
p=R/'s03.patch.json'; basep=R/'baseline.json'; reviewp=R/'s03.review.md'
patch=json.loads(p.read_text(encoding='utf-8')); baseline=json.loads(basep.read_text(encoding='utf-8'))
baseline_blocks={b['id']:b for b in baseline['blocks']}
updates=patch['updates']['blocks']; byid={b['id']:b for b in updates}
fixes={
 'history_book_01_p0082_b001':('xiRhWng','xiéháng'),
 'history_book_01_p0082_b010':('xiRhWng','xiéháng'),
 'history_book_01_p0083_b001':('bY','bó'),
 'history_book_01_p0083_b007':('bY','bó'),
 'history_book_01_p0095_b002':('sGu','sǒu'),
 'history_book_01_p0101_b004':('yP','yú'),
}
for bid,(old,new) in fixes.items():
 if bid not in byid:
  byid[bid]=copy.deepcopy(baseline_blocks[bid])
 block=byid[bid]
 before=block.get('clean_text') or ''
 assert old in before,(bid,old)
 block['clean_text']=before.replace(old,new)
 # raw_text is copied from or kept identical to baseline.
 assert block.get('raw_text')==baseline_blocks[bid].get('raw_text'),bid
# keep deterministic order by block id, while retaining all pre-existing block updates
patch['updates']['blocks']=sorted(byid.values(),key=lambda b:b['id'])
p.write_text(json.dumps(patch,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
addendum='''\n\n- 拼音OCR主审补记（图像依据：`primary/ocr/`，原书PDF第82、83、95、101页高分辨率截图及对应裁切）：逐字核读声调后，修正 `clean_text` 中 6 个重复/独立block：p0082_b001、b010“颉颃（xiéháng）”；p0083_b001、b007“踣（bó）”；p0095_b002“渊薮（sǒu）”；p0101_b004“徐继畬（yú）”。`raw_text` 全部保持原值。未改knowledge或其他patch内容。\n'''
text=reviewp.read_text(encoding='utf-8')
if '拼音OCR主审补记' not in text: reviewp.write_text(text+addendum,encoding='utf-8')
print('updated blocks',len(patch['updates']['blocks']),'targeted',len(fixes))
