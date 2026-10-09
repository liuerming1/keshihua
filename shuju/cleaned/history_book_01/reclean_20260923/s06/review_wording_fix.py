from pathlib import Path
p=Path('shuju/cleaned/history_book_01/reclean_20260923/s06/make_patch.py')
s=p.read_text(encoding='utf-8-sig')
s=s.replace("37条水印block更新只改clean_text且raw_text不变", "37条水印block在clean_text中去除乱码、raw_text保持不变，并有新增复核标记")
s=s.replace("' 教材1127—1276与外部补充1279已在summary/time中按来源归属区分，保留原verification/finalization字段。'", "' 教材1127—1276与外部补充1279已在summary/time中按来源归属区分，保留原verification/finalization字段'")
s=s.replace("' 本次补入了原文明确的背景/影响Claim及对应块。'", "' 本次补入了原文明确的背景/影响Claim及对应块。'")
s=s.replace("只改clean_text且raw_text不变", "只在clean_text删除水印，raw_text不变")
p.write_text(s,encoding='utf-8')
