from pathlib import Path
p=Path('shuju/cleaned/history_book_01/reclean_20260923/s06/make_patch.py')
s=p.read_text(encoding='utf-8-sig')
needle="k['background']=claim('教材将1984—1988年经济加速发展置于全面改革推动之下。',['history_book_01_p0188_b004'])\nk['points']=["
repl="k['title']='1983—1991年经济与科技成就'\nk['summary']=claim('全面改革推动1984—1988年经济加速，1990年“七五”计划多数指标完成或超额完成；1983、1988、1991年先后取得巨型计算机、北京正负电子对撞机和秦山核电站成果。',['history_book_01_p0188_b004'])\nk['background']=claim('教材将1984—1988年经济加速发展置于全面改革推动之下。',['history_book_01_p0188_b004'])\nk['points']=["
assert needle in s
p.write_text(s.replace(needle,repl),encoding='utf-8')
