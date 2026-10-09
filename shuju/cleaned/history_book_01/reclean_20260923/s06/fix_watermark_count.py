from pathlib import Path
p=Path('shuju/cleaned/history_book_01/reclean_20260923/s06/make_patch.py')
s=p.read_text(encoding='utf-8-sig')
s=s.replace("assert len(block_updates)==37, f'expected one page-bottom watermark block for each page, got {len(block_updates)}'", "assert len(block_updates)==37, f'expected all contaminated blocks, got {len(block_updates)}'\nwatermark_pages=sorted({int(__import__('re').search(r'_p(\\d{4})_b',b['id']).group(1)) for b in block_updates})\nassert watermark_pages==list(range(187,215)), watermark_pages")
s=s.replace("37页整页底稿clean_text移除页尾NÅO水印乱码", "37个整页底稿block的clean_text移除页尾NÅO水印乱码（覆盖页187–214，其中197–205另有重复底稿block）")
s=s.replace("'- 水印清理：37个页末底稿block的clean_text去除NÅO加二进制尾码，raw_text未变；受影响block ID列在updates.blocks。'", "'- 水印清理：37个页末底稿block的clean_text去除NÅO加二进制尾码，覆盖PDF页187–214；页197–205各有两个包含同一页底稿的block。raw_text未变，受影响block ID列在updates.blocks。'")
s=s.replace("37条水印更新只改clean_text且raw_text不变", "37条水印block更新只改clean_text且raw_text不变")
p.write_text(s,encoding='utf-8')
