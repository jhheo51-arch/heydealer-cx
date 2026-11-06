"""App Store와 Google Play 리뷰를 같은 기간으로 맞춰 별점과 1~3점 주제를 비교한다.
필요: heydealer_reviews.json (collect.py), heydealer_reviews_appstore.json (collect_appstore.py)
원문은 출력하지 않는다. 결과 정리는 appstore_compare.md
"""
import json, re
from collections import Counter
src = open('classify.py', encoding='utf-8').read()
RULES = eval(re.search(r'RULES = (\[.*?\n\])', src, re.S).group(1))
def topic(t):
    for n, p in RULES:
        if re.search(p, t): return n
    return '기타'
a = json.load(open('heydealer_reviews_appstore.json', encoding='utf-8'))
g = json.load(open('heydealer_reviews.json', encoding='utf-8'))
start = min(x['at'][:10] for x in a)
gp = [x for x in g if x['at'][:10] >= start]
for name, rows, text in [('App Store', a, lambda r: r['title'] + ' ' + r['content']),
                         ('Google Play', gp, lambda r: r['content'] or '')]:
    c = Counter(r['score'] for r in rows); n = len(rows); low = [r for r in rows if r['score'] <= 3]
    print(name, n, min(r['at'][:10] for r in rows), '~', max(r['at'][:10] for r in rows))
    print('  별점', {k: c[k] for k in range(1, 6)}, '평균 %.2f' % (sum(r['score'] for r in rows) / n),
          '1~3점 %d (%.1f%%)' % (len(low), 100 * len(low) / n))
    print('  주제', Counter(topic(text(r)) for r in low).most_common())
