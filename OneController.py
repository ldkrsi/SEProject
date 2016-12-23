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
			#address=result.owner.pwd
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
		if request.form["password"]==User('0x56a9a02403bE71a4e44F9ff42f06E379A6E2fD27','12345678').pwd:
			ModelRoot.find_account(User('0x56a9a02403bE71a4e44F9ff42f06E379A6E2fD27','12345678')).upload_paper(request.form['paperlink'],request.form['hashcode'],request.form['metadata'])
			return render_template("單頁論文頁面.html")
		else:
			return(n)
	except:	
			return redirect(url_for("accountPage",address=address))
		
	
	
#修改個人資料頁面
@app.route("/<address>/update",methods=["GET"])
def updatePage(address):
	return render_template("修改個人資料頁面.html",Address=ModelRoot.find_account(User('0x56a9a02403bE71a4e44F9ff42f06E379A6E2fD27')).infomation()['owner'],accountAddr=address)
@app.route("/<address>/update",methods=["POST"])
def update(address):
	try:
		'''修改個人資料'''
		return redirect(url_for("accountPage",address=address))
	except:
		return redirect(url_for("accountPage",address=address))


#論文列表頁面
@app.route("/<address>/papers",methods=["GET"])
def papers(address):
	user=ModelRoot.find_account(User('0x56a9a02403bE71a4e44F9ff42f06E379A6E2fD27'));
	
	if len(ModelRoot.find_account(User('0x56a9a02403bE71a4e44F9ff42f06E379A6E2fD27')).papers_list())>0:
		p=len(ModelRoot.find_account(User('0x56a9a02403bE71a4e44F9ff42f06E379A6E2fD27')).papers_list())-1;
	
	link=[]
	hashcode=[]
	metadata=[]
	for i in range(p):
		link.append(user.papers_list()[i].read_data().doc_info()[0])
		hashcode.append(user.papers_list()[i].read_data().doc_info()[1])
		metadata.append(user.papers_list()[i].read_data().metadata())
	return render_template("論文列表頁面.html",Address=user.infomation()['owner'],accountAddr=address,p=p,link=link,hashcode=hashcode,metadata=metadata)
	
	

#邀請申請頁面
@app.route("/<address>/invite",methods=["GET"])
def invite(address):
		return render_template("邀請申請頁面.html",Address=ModelRoot.find_account(User('0x56a9a02403bE71a4e44F9ff42f06E379A6E2fD27')).infomation()['owner'],accountAddr=address)

	
#查看所有發出的邀請頁面
@app.route("/<address>/invites",methods=["GET"])
def invites(address):
	return render_template("查看所有發出的邀請頁面.html",Address=ModelRoot.find_account(User('0x56a9a02403bE71a4e44F9ff42f06E379A6E2fD27')).infomation()['owner'],accountAddr=address)
	
#查看所有收到的邀請頁面
@app.route("/<address>/requests",methods=["GET"])
def requests(address):
	return render_template("查看所有收到的邀請頁面.html",Address=ModelRoot.find_account(User('0x56a9a02403bE71a4e44F9ff42f06E379A6E2fD27')).infomation()['owner'],accountAddr=address)


if __name__=="__main__":	
	app.run(debug=True)