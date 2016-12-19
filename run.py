from BaseController import *
import OneController, TwoController



@app.route('/example/<account_address>')
def example(account_address):
	one = ModelRoot.get_my_account(User(account_address))
	p = one.papers_list()[0].infomation()
	p['belong to'] = p['belong to'].address
	i = one.invites_list()[0].infomation()
	i['reviewer'] = i['reviewer'].address
	i['sender'] = i['sender'].address
	i['paper'] = i['paper'].address
	return str(p)+'<br>'+str(i)

@app.route('/transactions')
def transactions():
	from model import rds,web3
	from flask import render_template
	import json, datetime

	data_list = sorted(rds.keys(),reverse=True)
	result = []
	for key in data_list:
		value = json.loads(rds.get(key).decode('utf-8'))
		if value[0] is False:
			ans = web3.eth.getTransactionReceipt(value[1])
			value[0] = True if ans is not None else False
			rds.set(key,json.dumps(value))
		result.append([
			datetime.datetime.fromtimestamp(
				int(float(key.decode('utf-8')))
			).strftime('%Y-%m-%dT%H:%M:%SZ'),
			value
		])
	return render_template('transactions.html', result=result)

if __name__ == "__main__":
	app.run(host= '0.0.0.0')
