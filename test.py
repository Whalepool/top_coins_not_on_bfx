from pprint import pprint

from wpbfx import WpBFX
from wpcoingecko import WpCoinGecko

bfx = WpBFX()
coingecko = WpCoinGecko()


"""
Get the top 100 coins from coingecko
"""
top_cmc = coingecko.coins_markets( {'vs_currency': 'usd', 'order':'market_cap_desc', 'per_page': 100})
top_cmc_dict = {}
ignore = ['MIOTA','USDT','BNB']
for i, m in enumerate(top_cmc):
	symbol = m['symbol'].upper()
	if symbol in ignore:
		continue

	top_cmc_dict[symbol] = i


"""
Get the top trending coins from coingecko
"""
trending = coingecko.trending()
top_trending = {}
for i, c in enumerate(trending['coins']):

	top_trending[ c['item']['symbol'] ] = i 


""" 
Get the bfx api->ticker maps
"""
map_curr_sym = bfx.map_curr_sym()
bfx_tickers = {}
for m in map_curr_sym[0]:
	for i, el in enumerate(m):
		if el[:4] == 'AAA':
			continue
		if el[:4] == 'BBB':
			continue
		if el[:4] == 'TEST':
			continue
		if el[-2:] == 'F0':
			continue
		if el[-1:] == 't':
			continue
		if el[-2:] == 't0':
			continue

		if i == 0: 
			bfx_tickers[el] = m[1]
		if i == 1:
			bfx_tickers[el] = m[0]


"""
Get the bfx api tickers
""" 
tickers = bfx.get_tickers()
for t in tickers:
	symbol = t[0]
	if symbol[0] != 't':
		continue 

	symbol = symbol[1:]
	split = symbol.split(':')
	if len(split) > 1:
		fp = split[0]
	else:
		fp = symbol[:3]

	if fp[-2:] == 'F0':
		continue

	if fp[:4] == 'AAA':
		continue
	if fp[:4] == 'BBB':
		continue

	if fp[:4] == 'TEST':
		continue

	if fp in bfx_tickers:
		continue

	bfx_tickers[ fp ] = fp

	# pprint(symbol+' '+str(split))


missing = {}
missing['mc'] = {}
missing['trending'] = {}

""" 
Check for missing top marketcap tickers
"""
for symbol,i in top_cmc_dict.items():

	if symbol not in bfx_tickers: 
		missing['mc'][symbol] = i 

""" 
Check for missing top trending tickers
"""
for symbol,i in top_trending.items():

	if symbol not in bfx_tickers: 
		missing['trending'][symbol] = i 


out = ""
out += "Top 100 market cap coins \n"

so = sorted(missing['mc'].items(), key=lambda x: x[1])
for s in so:

	symbol = s[0]
	i = s[1]
	info = top_cmc[i] 

	gor = ''
	if info['price_change_percentage_24h'] > 0:
		gor = '+'
	else:
		gor = ''

	out += "{:>20.20} ({:^6}) - ${:4.0f}m  ".format(info['name'], symbol, info['market_cap']/1000000) 
	out += "{:>2}{:3.0f}%".format(gor,info['price_change_percentage_24h']) 
	out += "\n"


out += "\n"
out += "Top trending coins \n"

so = sorted(missing['trending'].items(), key=lambda x: x[1]) 
for s in so:

	symbol = s[0]

	if symbol in top_cmc_dict:
		i = top_cmc_dict[symbol]
		info = top_cmc[i] 
	
		gor = ''
		if info['price_change_percentage_24h'] > 0:
			gor = '+'
		else:
			gor = ''

		out += "{:>20.20} - ${:4.0f}m".format(symbol, info['market_cap']/1000000, info['price_change_percentage_24h']) 
		out += "{:>2}{:3.0f}%".format(gor,info['price_change_percentage_24h']) 
		out += "\n"

	else:

		out += "{:>20.20} - Not yet in top 100 market cap".format( symbol ) 
		out += "\n"


print(out)
exit()