import json
from google_play_scraper import reviews, Sort
out=[]; token=None
for _ in range(30):
    r, token = reviews('kr.perfectree.heydealer', lang='ko', country='kr', sort=Sort.NEWEST, count=200, continuation_token=token)
    out += r
    if not token or not r: break
for x in out: x['at']=x['at'].isoformat(); x.pop('userName',None); x.pop('userImage',None); x.pop('repliedAt',None) if False else None
for x in out:
    if x.get('repliedAt'): x['repliedAt']=x['repliedAt'].isoformat()
json.dump(out, open('heydealer_reviews.json','w',encoding='utf-8'), ensure_ascii=False, indent=0)
print(len(out), out[-1]['at'][:10], out[0]['at'][:10])
