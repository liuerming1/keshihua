import json
p='shuju/cleaned/history_book_01/reclean_20260923/baseline.json'; d=json.load(open(p,encoding='utf-8'))
ids=['history_book_01_p0119','history_book_01_p0120','history_book_01_p0121','history_book_01_p0126','history_book_01_p0127','history_book_01_p0129','history_book_01_p0132','history_book_01_p0133','history_book_01_p0145','history_book_01_p0146']
for page in d['pages']:
 if page['id'] in ids:
  print('PAGE',page['id'])
  for b in sorted([b for b in d['blocks'] if b['page_id']==page['id']],key=lambda x:x['order']): print(b['id'],b['type'],(b.get('clean_text') or '')[:220].replace('\n',' '))
