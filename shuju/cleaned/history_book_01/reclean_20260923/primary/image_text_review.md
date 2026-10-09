# 六张教材图片的文字复核

复核对象为已导出的教材资产PNG；同时查看对应PDF原页600dpi裁切。`file_path`、`bbox`、`export`完整保留，所有文件SHA-256与资产记录一致。状态仅描述图片内文字识读覆盖：完整、部分可辨或不可辨。

| 资产 | 状态 | 已读内容与限制 | 图像证据 |
|---|---|---|---|
| `history_book_01_p0030_a001` | `partial` | 已核对导出地图PNG和原PDF第30页600dpi裁切。西汉、主要部族/地名及图例中可辨项目与visible_text所列相符；边缘密集小字和局部模糊地名未逐一可靠确认，因此只保留已辨认项目，不宣称完整转录。 | `public/textbook-assets/history_book_01_p0030_a001.png`, `primary/ocr/history_book_01_p0030_a001_pdf600.png`, `primary/ocr/p0030_map_tl.png`, `primary/ocr/p0030_map_tr.png`, `primary/ocr/p0030_map_bl.png`, `primary/ocr/p0030_map_br.png` |
| `history_book_01_p0032_a001` | `partial` | 已核对导出书影和原PDF第32页600dpi裁切。可确认书影为《九章算术》；封面其余竖排小字因原图颗粒、磨损和分辨率限制不能逐字可靠辨认，不据此判断版本。 | `public/textbook-assets/history_book_01_p0032_a001.png`, `primary/ocr/history_book_01_p0032_a001_pdf600.png` |
| `history_book_01_p0038_a002` | `unreadable` | 已核对导出照片和原PDF第38页600dpi裁切。石壁表面确为题注所指祝文照片，但刻字在导出图和原页扫描中均无法辨认成可确认的字词；题注只确认地点/内容类型，不把题注当作祝文转录。 | `public/textbook-assets/history_book_01_p0038_a002.png`, `primary/ocr/history_book_01_p0038_a002_pdf600.png` |
| `history_book_01_p0157_a001` | `unreadable` | 已核对报纸导出图和原PDF第157页600dpi裁切。报纸版面上的标题、正文小字均因原照片尺寸与清晰度不足无法可靠逐字辨认；图注仅确认这是“当时报纸关于接收的报道”，不据此补写报纸内容。 | `public/textbook-assets/history_book_01_p0157_a001.png`, `primary/ocr/history_book_01_p0157_a001_pdf600.png` |
| `history_book_01_p0178_a003` | `partial` | 已核对日记导出图和原PDF第178页600dpi裁切。手写影像首句可辨为“我是个普通工人”，其余手写内容笔画小且模糊，不能可靠逐字转录；visible_text中的省略号明确表示未读全。 | `public/textbook-assets/history_book_01_p0178_a003.png`, `primary/ocr/history_book_01_p0178_a003_pdf600.png` |
| `history_book_01_p0182_a001` | `partial` | 已核对报纸导出图和原PDF第182页600dpi裁切。报头照片中的标题“实践是检验真理的唯一标准”可辨；报纸栏内正文小字不具备可靠逐字识读条件，因此visible_text只保留标题。 | `public/textbook-assets/history_book_01_p0182_a001.png`, `primary/ocr/history_book_01_p0182_a001_pdf600.png` |

高分辨率重渲染不能恢复原扫描中已经缺失的笔画。凡无法可靠辨认的刻字、报纸正文及封面小字均留作不可辨/部分可辨，不按图注或历史常识伪造转录。报纸、日记PNG均已存在；此前“未导出”的旧备注已由本复核备注替换。

## 主代理二次目视复核（2026-09-24，覆盖上表两项初审结论）

- p0178_a003：五行文字在原图和600dpi裁切中可读，已完整逐行转录，“我是个普通工人没啥……小本本上只能记差距。”；改complete，仅对应图片所示内容。
- p0157_a001：两条大标题“广州‘接收’一片混乱”“北平情况非常混乱”可读，已按简体记录；其余小字仍不能可靠全录，改partial。
