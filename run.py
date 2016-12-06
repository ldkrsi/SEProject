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

if __name__ == "__main__":
	app.run(host= '0.0.0.0')
