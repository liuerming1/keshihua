from pathlib import Path
p=Path('shuju/cleaned/history_book_01/reclean_20260923/s06/make_patch.py')
s=p.read_text(encoding='utf-8-sig')
s=s.replace("'p198正文续至思想理论定位，p199继续大会主题及新时代十年三件大事，主题与主体正文各自在页块中完整。','复核p198页尾、p199页首；未把相邻页自动当成同一句续文，确认p199本块承接同一章节但句段边界独立。','保留两块作为章节连续性证据，不合并成一个句子。'", "'p198页末“大”字与p199页首“会的主题是”组成跨页词语“大会”。','对照页尾和页首文字层及渲染图，确认词语跨页接续。','按原文次序保留p198、p199两个证据块。'")
p.write_text(s,encoding='utf-8')
