from BaseController import *

@app.route('/one')
def function_one():
    return 'one'

@app.route("/",methods=["GET"])
def index():
	return render_template("首頁.html")
	
@app.route("/",methods=["POST"])
def createOrSearch():
	if 'createaccount' in request.form:
		#創帳號
		return "2"
	elif 'searchaccount' in request.form:
		#找帳號
		result=ModelRoot.find_account(User(request.form['searchaccount']))
		#失敗
		if result is None:
			return render_template("帳號頁面.html")
		#成功
		else:
			EtherAddress=request.form['searchaccount']
			address=result.address
			return redirect(url_for("accountPage",address=address))

			
#帳號頁面
@app.route("/<address>/",methods=["GET"])
def accountPage(address):
	return render_template("帳號頁面.html",Address=ModelRoot.find_account(User('0x56a9a02403bE71a4e44F9ff42f06E379A6E2fD27')).infomation()['owner'],accountAddr=address)

	
#上傳論文頁面
@app.route("/<address>/upload",methods=["GET"])
def uploadPage(address):
	return render_template("上傳論文頁面.html",Address=ModelRoot.find_account(User('0x56a9a02403bE71a4e44F9ff42f06E379A6E2fD27')).infomation()['owner'],accountAddr=address)

@app.route("/<address>/upload",methods=["POST"])
def upload(address):
	try:
		ModelRoot.find_account(User('0x56a9a02403bE71a4e44F9ff42f06E379A6E2fD27','12345678')).upload_paper(request.form['paperlink'],request.form['hashcode'],request.form['metadata'])
	
	except:	
		return render_template("帳號頁面.html",Address=ModelRoot.find_account(User('0x56a9a02403bE71a4e44F9ff42f06E379A6E2fD27')).infomation()['owner'],accountAddr=address)
		
	return render_template("單頁論文頁面.html")
	
	
#修改個人資料頁面
@app.route("/<address>/update",methods=["GET"])
def update(address):
	return render_template("修改個人資料頁面.html",Address=ModelRoot.find_account(User('0x56a9a02403bE71a4e44F9ff42f06E379A6E2fD27')).infomation()['owner'],accountAddr=address)


#論文列表
@app.route("/<address>/papers",methods=["GET"])
def papers(address):
	return render_template("論文列表頁面.html",Address=ModelRoot.find_account(User('0x56a9a02403bE71a4e44F9ff42f06E379A6E2fD27')).infomation()['owner'],accountAddr=address)

#查看所有發出的邀請頁面
@app.route("/<address>/invites",methods=["GET"])
def invites(address):
	return render_template("查看所有發出的邀請頁面.html",Address=ModelRoot.find_account(User('0x56a9a02403bE71a4e44F9ff42f06E379A6E2fD27')).infomation()['owner'],accountAddr=address)
	
#查看所有收到的邀請頁面
@app.route("/<address>/requests",methods=["GET"])
def requests(address):
	return render_template("查看所有收到的邀請頁面.html",Address=ModelRoot.find_account(User('0x56a9a02403bE71a4e44F9ff42f06E379A6E2fD27')).infomation()['owner'],accountAddr=address)


	
	
'''	

							
		result=modelroot.find(帳號)
		if result is None:
			return render_template("首頁.html")
		else:
			return render_template("帳號頁面.html")
	'''
#	return request.form["name"]
'''
	address=app.request
	usr=usr
	result=modelroot.find(帳號)
	if result is None:
		return "首頁網址"
	else:
		return "帳號頁面"
'''		
if __name__=="__main__":	
	app.run(debug=True)