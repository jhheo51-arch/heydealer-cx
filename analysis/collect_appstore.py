"""헤이딜러 iOS 앱(App Store id 980166975) 한국 리뷰 수집.
Apple 공개 RSS는 최신순 최대 10쪽(쪽당 50건)까지만 준다. 작성자 이름은 저장하지 않는다.
결과: heydealer_reviews_appstore.json (저장소에는 올리지 않음)
"""
import json, urllib.request
out = []
for page in range(1, 11):
    url = f'https://itunes.apple.com/kr/rss/customerreviews/page={page}/id=980166975/sortby=mostrecent/json'
    try:
        d = json.load(urllib.request.urlopen(url, timeout=20))
    except Exception as e:
        print('stop', page, e); break
    entries = d.get('feed', {}).get('entry', [])
    if isinstance(entries, dict): entries = [entries]
    entries = [e for e in entries if 'im:rating' in e]
    if not entries: break
    for e in entries:
        out.append({'at': e['updated']['label'], 'score': int(e['im:rating']['label']),
                    'title': e['title']['label'], 'content': e['content']['label'],
                    'version': e.get('im:version', {}).get('label')})
json.dump(out, open('heydealer_reviews_appstore.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print(len(out), out[-1]['at'][:10] if out else '', out[0]['at'][:10] if out else '')
