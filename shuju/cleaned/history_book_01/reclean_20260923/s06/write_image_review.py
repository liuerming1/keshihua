import json,hashlib,copy
from pathlib import Path
R=Path('shuju/cleaned/history_book_01/reclean_20260923'); primary=R/'primary'; primary.mkdir(exist_ok=True)
D=json.loads((R/'baseline.json').read_text(encoding='utf-8')); all_assets={a['id']:a for a in D['assets']}
items=[
('history_book_01_p0030_a001','partial',[
 'public/textbook-assets/history_book_01_p0030_a001.png',
 'primary/ocr/history_book_01_p0030_a001_pdf600.png',
 'primary/ocr/p0030_map_tl.png','primary/ocr/p0030_map_tr.png','primary/ocr/p0030_map_bl.png','primary/ocr/p0030_map_br.png'],
 '已核对导出地图PNG和原PDF第30页600dpi裁切。西汉、主要部族/地名及图例中可辨项目与visible_text所列相符；边缘密集小字和局部模糊地名未逐一可靠确认，因此只保留已辨认项目，不宣称完整转录。',
 ['地图内小字按原页600dpi图像读取可辨部分并列在visible_text；边缘与密集标注仍有未辨清处，地名清单不声称完整。']),
('history_book_01_p0032_a001','partial',[
 'public/textbook-assets/history_book_01_p0032_a001.png','primary/ocr/history_book_01_p0032_a001_pdf600.png'],
 '已核对导出书影和原PDF第32页600dpi裁切。可确认书影为《九章算术》；封面其余竖排小字因原图颗粒、磨损和分辨率限制不能逐字可靠辨认，不据此判断版本。',
 ['已检查导出书影及原页600dpi裁切；题名《九章算术》可确认，封面其余细字未能可靠逐字识读，未推定版本。']),
('history_book_01_p0038_a002','unreadable',[
 'public/textbook-assets/history_book_01_p0038_a002.png','primary/ocr/history_book_01_p0038_a002_pdf600.png'],
 '已核对导出照片和原PDF第38页600dpi裁切。石壁表面确为题注所指祝文照片，但刻字在导出图和原页扫描中均无法辨认成可确认的字词；题注只确认地点/内容类型，不把题注当作祝文转录。',
 ['已核对导出图与原页600dpi裁切；石壁刻文具体字词不可辨，题注可确认其为“鲜卑旧墟石室嘎仙洞祝文”，未转录刻文。']),
('history_book_01_p0157_a001','unreadable',[
 'public/textbook-assets/history_book_01_p0157_a001.png','primary/ocr/history_book_01_p0157_a001_pdf600.png'],
 '已核对报纸导出图和原PDF第157页600dpi裁切。报纸版面上的标题、正文小字均因原照片尺寸与清晰度不足无法可靠逐字辨认；图注仅确认这是“当时报纸关于接收的报道”，不据此补写报纸内容。',
 ['报纸PNG确已导出并逐字检查；报纸自身标题/正文在源图中不可可靠辨认，visible_text保持null。图注确认其主题，不能替代报纸原文。']),
('history_book_01_p0178_a003','partial',[
 'public/textbook-assets/history_book_01_p0178_a003.png','primary/ocr/history_book_01_p0178_a003_pdf600.png'],
 '已核对日记导出图和原PDF第178页600dpi裁切。手写影像首句可辨为“我是个普通工人”，其余手写内容笔画小且模糊，不能可靠逐字转录；visible_text中的省略号明确表示未读全。',
 ['日记PNG已导出且核对原页600dpi裁切；仅确认开头“我是个普通工人”，后续手写字无法完整辨认，未补写全文。']),
('history_book_01_p0182_a001','partial',[
 'public/textbook-assets/history_book_01_p0182_a001.png','primary/ocr/history_book_01_p0182_a001_pdf600.png'],
 '已核对报纸导出图和原PDF第182页600dpi裁切。报头照片中的标题“实践是检验真理的唯一标准”可辨；报纸栏内正文小字不具备可靠逐字识读条件，因此visible_text只保留标题。',
 ['报纸PNG已导出；原页600dpi裁切可核读标题“实践是检验真理的唯一标准”，栏内正文小字仍不可可靠逐字识读。'])]
updates=[]
for aid,status,evidence,note,newnotes in items:
 a=copy.deepcopy(all_assets[aid])
 a['notes']=newnotes
 if aid=='history_book_01_p0038_a002': a['visible_text']=None
 a['text_review']={'status':status,'evidence':evidence,'note':note}
 # ensure critical artifact-location/export metadata was not altered
 orig=all_assets[aid]
 for key in ['file_path','bbox','export']:
  assert a[key]==orig[key],(aid,key)
 path=Path('public')/a['file_path'].lstrip('/')
 assert path.exists(),path
 h=hashlib.sha256(path.read_bytes()).hexdigest(); assert h==a['export']['sha256'],(aid,h,a['export']['sha256'])
 updates.append(a)
(primary/'image_text_review.json').write_text(json.dumps(updates,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['# 六张教材图片的文字复核','', '复核对象为已导出的教材资产PNG；同时查看对应PDF原页600dpi裁切。`file_path`、`bbox`、`export`完整保留，所有文件SHA-256与资产记录一致。状态仅描述图片内文字识读覆盖：完整、部分可辨或不可辨。', '', '| 资产 | 状态 | 已读内容与限制 | 图像证据 |','|---|---|---|---|']
for aid,status,evidence,note,_ in items:
 lines.append(f"| `{aid}` | `{status}` | {note} | {', '.join('`'+x+'`' for x in evidence)} |")
lines += ['', '高分辨率重渲染不能恢复原扫描中已经缺失的笔画。凡无法可靠辨认的刻字、报纸正文及封面小字均留作不可辨/部分可辨，不按图注或历史常识伪造转录。报纸、日记PNG均已存在；此前“未导出”的旧备注已由本复核备注替换。']
(primary/'image_text_review.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('wrote',len(updates),'assets')
