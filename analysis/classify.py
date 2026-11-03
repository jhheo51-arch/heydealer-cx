"""헤이딜러 앱 리뷰 1~3점 452건 분류.
1) 규칙(키워드)으로 주제를 하나 붙인다. 위에서부터 먼저 맞는 주제를 쓴다.
2) 차를 산 사람의 리뷰(구매 여정)는 사람이 직접 읽고 VOC 유형과 여정 단계를 붙였다(MANUAL).
결과: coded_low.csv, summary.json
"""
import json, re, csv
from collections import Counter

r = json.load(open('heydealer_reviews.json', encoding='utf-8'))

RULES = [
    ('고객센터 연결', r'고객센터|상담|채팅|챗|연락이? ?(안|없)|통화|전화 ?연결|연락안|답변'),
    ('판매 가격과 감가', r'감가|후려|견적|입찰|경매|최고가|시세|가격|딜러|매입|깍|깎|낙찰|제로'),
    ('앱 오류와 속도', r'앱|어플|실행|접속|로딩|팅기|튕|강제종료|업데이트|느림|느려|먹통|오류|에러|다운'),
    ('명의이전과 탁송', r'명의|탁송|통행료|서류|말소|인수기사'),
    ('이력조회와 개인정보', r'이력|조회|번호판|차번호|개인정보|소유자'),
    ('광고와 이벤트', r'광고|이벤트|모델|공유|응모|0하나|영빼기'),
]

# 차를 사는 쪽 리뷰: 직접 읽고 붙인 값 (index: (VOC 유형, 여정 단계, 한 줄 요약))
MANUAL = {
    297: ('정비와 수리', '정비와 보상', '구매 2일 뒤 브레이크 이상, 보험 수리 일부만 승인, 부품 지연 후 연락 없음'),
    360: ('성능점검', '이상 발견', '인수 전 검수에서 도어 버튼 고장 누락, 하부 검수 범위가 광고와 다름, 오래된 차는 안심케어 제외'),
    578: ('보증 범위', '보증 문의', '쇼바 결함을 소모품이라며 1년 보증 거절, 상담 요청이 계속 끊김'),
    1255: ('정보 설명 부족', '구매 결정', '구매 전 내 지역 보증수리 가능 여부를 알려 주지 않음'),
    1271: ('차량 상태', '이상 발견', '점검과 달리 휠하우스 교환 사고차, 채팅 오류와 전화 불통'),
    780: ('정보 설명 부족', '정보 확인', '엔진룸 사진 추가 요청이 반영되지 않음'),
    778: ('정보 설명 부족', '차량 탐색', '오래된 연식 매물이 없음'),
    287: ('가격과 견적', '차량 탐색', '매물이 적고 가격이 비쌈'),
    1383: ('가격과 견적', '차량 탐색', '매물이 적고 비쌈'),
    588: ('가격과 견적', '차량 탐색', '살 때 원하는 가격대 매물이 없음'),
    1279: ('처리 지연', '차량 탐색', '내차사기 매물 화면이 너무 느림'),
    1336: ('정보 설명 부족', '차량 탐색', '검색 결과 10대 이후 스크롤 안 됨'),
    1341: ('환불과 계약', '구매 결정', '신용카드 할부 결제가 안 됨'),
    2152: ('상담 태도', '구매 결정', '차를 사려는데 카톡과 연락처가 없음'),
    1329: ('정보 설명 부족', '정보 확인', '최근 1년 보험이력이 나오지 않음'),
    2015: ('정보 설명 부족', '정보 확인', '이력조회에 소유자 이름이 필요해 살 차를 확인하기 어려움'),
    430: ('정보 설명 부족', '차량 탐색', '차량을 고르기 전에는 옵션 필터를 쓸 수 없음'),
    3705: ('가격과 견적', '차량 탐색', '매물이 너무 없음'),
    4258: ('가격과 견적', '차량 탐색', '내차사기 매물이 173대뿐'),
    5069: ('가격과 견적', '차량 탐색', '중고 매물이 너무 없음'),
    795: ('처리 지연', '차량 탐색', '내차사기 화면이 열리지 않음'),
}
# 5점, 4점 중 구매 경험 리뷰(대조용)
POSITIVE_BUY = {
    1227: '1년 케어로 수리비를 바로 지급받음',
    1287: '인증중고차 구매가 편했음',
    1038: '사진이 자세해 반품 걱정이 줄었음, 매물은 적음',
}

def topic(text):
    for name, pat in RULES:
        if re.search(pat, text):
            return name
    return '기타'

rows = []
for i, x in enumerate(r):
    if x['score'] > 3:
        continue
    t = x['content'].replace('\n', ' ')
    m = MANUAL.get(i)
    rows.append({
        'idx': i, 'date': x['at'][:10], 'score': x['score'],
        'replied': 1 if x.get('replyContent') else 0,
        'topic': '차량 구매와 사후 처리' if m else topic(t),
        'voc_type': m[0] if m else '', 'journey': m[1] if m else '',
        'note': m[2] if m else '', 'text': t,
    })

with open('coded_low.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)

stars = Counter(x['score'] for x in r)
summary = {
    'total': len(r), 'period': [min(x['at'] for x in r)[:10], max(x['at'] for x in r)[:10]],
    'stars': dict(sorted(stars.items())), 'low': len(rows),
    'low_replied': sum(x['replied'] for x in rows),
    'topics': Counter(x['topic'] for x in rows).most_common(),
    'buy_voc': Counter(x['voc_type'] for x in rows if x['voc_type']).most_common(),
    'buy_journey': Counter(x['journey'] for x in rows if x['journey']).most_common(),
    'positive_buy': POSITIVE_BUY,
}
json.dump(summary, open('summary.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(summary, ensure_ascii=False, indent=1))
