import requests
from lxml import etree

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
	'Cookie': 's=dh11011m96; __utmz=1.1588941541.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); device_id=98c19176442315a18d4e970942339d43; bid=b0a8d8e5cc7bf579e1ea43cfd0a85c52_kabvgny8; aliyungf_tc=AQAAAF/hXjMXAw0AC4SLdbChzAjKh6pG; xq_a_token=69a6c81b73f854a856169c9aab6cd45348ae1299; xq_r_token=08a169936f6c0c1b6ee5078ea407bb28f28efecf; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTU5ODMyMzAwNCwiY3RtIjoxNTk2ODgwMTg3NTg4LCJjaWQiOiJkOWQwbjRBWnVwIn0.ImRB1Fcr4NJ3lKvjd5x3fcas99KEMrg_XqPboB2PrdRwwwi806_s-z-CN9PuBIT-6JoGbJuvVWb11z8KGDVkhRYd2tDPgaR8XLFEYztMs97CxSbUBfXxOi8HbkZIg-WRVneuYAVEzViRJHjxExdEyRlP1hPTL6hnG40-JIDFpRpLbKhM42cZ5QNgqld9k1OWCdRs72rKFErRrdBO1cp3LPya3vW1cFOImARK58pBNxbzwKwxtGZmZ7XCz2209RlNCWY6Xu3Z6kkVgvyu6civfkx5QLI104I2JGeg1-5H1nSSqk_Du8tg43sqBMQVYDngyz87KU7HyCHAh-oEV44oqA; Hm_lvt_1db88642e346389874251b5a1eded6e3=1595749209,1595856873,1595857172,1596880219; u=851596880219454; __utma=1.833849641.1588941541.1595857571.1596880219.8; __utmc=1; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1596882045; acw_tc=2760822d15968886597538797e54084fbc3f7d2b402d9bd9148bd5b360f13b'
}

def get(page):
	url = 'https://xueqiu.com/service/screener/screen?category=CN&exchange=sh_sz&areacode=&indcode=&order_by=roediluted.20191231&order=asc&page={page}&size=30&only_count=0&current=&pct=&pb=0_1.5&mc=0_2048858611800&dy_l=0.001_1700&pettm=0_25650.36&roediluted.20191231=10_1104.1&_=1596892246739'
	# url = 'https://xueqiu.com/service/screener/screen?category=CN&exchange=sh_sz&areacode=&indcode=&order_by=pb&order=asc&page={page}&size=30&only_count=0&current=&pct=&npay.20191231=0_13152.74&pettm=-12304.37_43943.99&pb=0_1.5&dy_l=0_14.98&_=1599143780651'
	r = requests.get(url.format(page=page), headers=headers)

	if r.status_code != 200:
		print(r.text)
		
	return r.json()['data']['list']

def cal(data, sort_field):
	for i, item in enumerate(data, 1):
		if sort_field == '市盈率' and item['pettm'] < 0:
			score = 482
		else:
			score = i

		if not item.get('score'):
			item['score'] = score
		else:
			item['score'] += score
		item[sort_field] = score
	

def deal(data, producy_limit=False):
	data.sort(key=lambda x: x['pb'])
	cal(data, '市净率')
	data.sort(key=lambda x: x['pettm'])
	cal(data, '市盈率')
	data.sort(key=lambda x: x['dy_l'], reverse=True)
	cal(data, '股息率')

	data.sort(key=lambda x: x['score'])

	if producy_limit:
		producy_limit = []
		for i in data:
			if producy_limit.count(i['indcode']) < 2:
				print(i)
				producy_limit.append(i['indcode'])
	else:
		for i in data:
			print(i)


data = []
for page in range(1, 17):
	data.extend(get(page))
for i in data:
	for k in ['pct', 'type', 'exchange', 'symbol', 'areacode', 'tick_size', 'has_follow', 'current', 'mc']:
		del i[k]
deal(data, False)
