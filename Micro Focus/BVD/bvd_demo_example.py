import requests
import re
import random
import datetime
import time

while True:

	cattle_url = "http://thestockmarketwatch.com/markets/commodities/commodity.aspx?item=/LE:US"
	cattle_out = requests.get(cattle_url)
	for cattle_match in re.finditer(r'qm_largequote">(\d+\.\d+)<', cattle_out.content, re.MULTILINE):
		cattle_price = float(cattle_match.group(1)) + random.randint(-5,5)
		cattle_json = {'last_price': cattle_price}
		cattle_to_bvd = requests.post('http://<your BVD server>:12224/api/submit/<your API ket>?tags=futures,cattle', json=cattle_json)
		
	
	oil_url = "http://thestockmarketwatch.com/markets/commodities/commodity.aspx?item=/CL:NMX"
	oil_out = requests.get(oil_url)
	for oil_match in re.finditer(r'qm_largequote">(\d+\.\d+)<', oil_out.content, re.MULTILINE):
		oil_price = float(oil_match.group(1)) + random.randint(-5,5)
		oil_json = {'last_price': oil_price}
		oil_to_bvd = requests.post('http://<your BVD server>:12224/api/submit/<your API ket>?tags=futures,oil', json=oil_json)
		
	print str(datetime.datetime.now()) + '\nSleeping for 300 seconds\n'
	time.sleep(300)
	