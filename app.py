from flask import Flask, render_template, request
import urllib, json
import datetime

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def getStockInfo():
	if request.method == 'GET':
		return render_template('pages/homepage.html')
	elif request.method == 'POST':
		print('----Drusti----')


	d = datetime.datetime.today()
	curr_date_time = d.strftime("%d-%B-%Y %H:%M:%S")
	print(curr_date_time)
	req_symbol = request.form['stockSymbol']
	uppercase_symbol = req_symbol.upper()
	try:
		api_url = "https://fmpcloud.io/api/v3/quote/" + uppercase_symbol + "?apikey=" + "15e8eb88f434e1f9ea9256891f8942c0"
	except urllib.error.URLError as e:
		data = {'error_reason': e.reason, 'error': 'We failed to reach the server'}
	except urllib.error.HTTPError as e:
		data = {'error_code': e, 'error': 'The server couln\'t fulfill the request'}
	else:
		response = urllib.request.urlopen(api_url)
		curr_data = json.loads(response.read())
		if len(curr_data) == 0:
			data = {'error': "Invalid Symbol"}
		else:
			company_name = curr_data[0]['name']
			price = curr_data[0]['price']
			change = curr_data[0]['change']
			percent_change = curr_data[0]['changesPercentage']
			data = {'curr_date': curr_date_time, 'company_name': company_name, 'price': price, 'change': change, 'percent_change': percent_change, 'stockSymbol': uppercase_symbol}
			print(data)
	
	return render_template('pages/homepage.html', **data)

if __name__ == "__main__":
	app.run()