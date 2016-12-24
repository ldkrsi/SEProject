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
			return render_template("首頁.html")
		#成功
		else:
			EtherAddress=request.form['searchaccount']
			address=result.address
			#address=result.owner.pwd
			return redirect(url_for("accountPage",address=address))

			
#帳號頁面
@app.route("/<address>/",methods=["GET"])
def accountPage(address):
	if address == 'favicon.ico':
		return '', 404
	result = Account(address)
	return render_template("帳號頁面.html",Address=result.infomation()['owner'],accountAddr=address,personinfo=result.infomation()['metadata'])

	
#上傳論文頁面
@app.route("/<address>/upload",methods=["GET"])
def uploadPage(address):
	result = Account(address)
	return render_template("上傳論文頁面.html",Address=result.infomation()['owner'],accountAddr=address)

@app.route("/<address>/upload",methods=["POST"])
def upload(address):
	try:
		a=User(result.infomation()['owner'],request.form["password"])
		result.upload_paper(request.form['paperlink'],request.form['hashcode'],request.form['metadata'])
		return redirect(url_for("transactions"))
	except:	
		return redirect(url_for("accountPage",address=address))
		
	
	
#修改個人資料頁面
@app.route("/<address>/update",methods=["GET"])
def updatePage(address):
	return render_template("修改個人資料頁面.html",Address=result.infomation()['owner'],accountAddr=address)
@app.route("/<address>/update",methods=["POST"])
def update(address):
	try:
		'''修改個人資料'''
		result.infomation()['metadata']=request.form['personinfo']
		
		return redirect(url_for("accountPage",address=address))
	except:
		return redirect(url_for("accountPage",address=address))


#論文列表頁面
@app.route("/<address>/papers",methods=["GET"])
def papers(address):	
	if len(result.papers_list())>0:
		p=len(result.papers_list())-1;
	link=[]
	hashcode=[]
	metadata=[]
	paperAddr=[]
	for i in range(p):
		link.append(result.papers_list()[i].read_data().doc_info()[0])
		hashcode.append(result.papers_list()[i].read_data().doc_info()[1])
		metadata.append(result.papers_list()[i].read_data().metadata())
		paperAddr.append(result.papers_list()[i].address)
	return render_template("論文列表頁面.html",Address=result.infomation()['owner'],
	accountAddr=address,p=p,link=link,hashcode=hashcode,metadata=metadata,paperAddr=paperAddr)

	
	
#單頁論文頁面
@app.route("/<address>/papers/<paperAddr>",methods=["GET"])
def paperPage(address,paperAddr):
	p=len(result.papers_list())-1;
	for i in range(p):
		if paperAddr==result.papers_list()[i].address:
			arthor=result.papers_list()[i].belog_to().address
			link=result.papers_list()[i].read_data().doc_info()[0]
			hashcode=result.papers_list()[i].read_data().doc_info()[1]
			time=result.papers_list()[i].read_data().doc_info()[2]
			metadata=result.papers_list()[i].read_data().metadata()
			break	
	return render_template("單頁論文頁面.html",arthor=arthor,link=link,hashcode=hashcode,time=time,metadata=metadata)


#邀請申請頁面
@app.route("/<address>/invite",methods=["GET"])
def invitePage(address):
	paperAddr=request.args.get('paper','')
	return render_template("邀請申請頁面.html",Address=result.infomation()['owner'],accountAddr=address,paperAddr=paperAddr)
@app.route("/<address>/invite",methods=["POST"])
def invite(address):
	toinvite=ModelRoot.find_account(User(request.form['toinvite']))
	price=request.form['price']
	i = two.invite_review(toinvite, result.papers_list()[0] ,price)
	return (i.infomation(), i.reviewer().address, i.sender().address, i.paper().infomation())

#查看所有發出的邀請頁面
@app.route("/<address>/invites",methods=["GET"])
def invitesPage(address):
	if len(result.invites_list())>0:
		p=len(result.invites_list())-1
	
	link=[]
	hashcode=[]
	metadata=[]
	reviewer=[]
	for i in range(p):
		link.append(result.invites_list()[i].paper().read_data().doc_info()[0])
		hashcode.append(result.invites_list()[i].paper().read_data().doc_info()[1])
		metadata.append(result.invites_list()[i].paper().read_data().metadata())
		reviewer.append(result.invites_list()[i].sender().address)
	return render_template("查看所有發出的邀請頁面.html",Address=result.infomation()['owner'],accountAddr=address,p=p,link=link,hashcode=hashcode,metadata=metadata,reviewer=reviewer)
@app.route("/<address>/invites",methods=["POST"])
def invites(address):	
	try:
		a=User(result.infomation()['owner'],request.form["password"])
		result.invites_list()[i].cancel_from()
		return redirect(url_for("transactions"))
	except:	
		return redirect(url_for("invitesPage",address=address))
#查看所有收到的邀請頁面
@app.route("/<address>/requests",methods=["GET"])
def requestsPage(address):
	if len(result.request_list())>0:
		p=len(result.request_list())-1
	
	link=[]
	hashcode=[]
	metadata=[]
	sender=[]
	inviteAddr=[]
	for i in range(p):
		link.append(result.request_list()[i].paper().read_data().doc_info()[0])
		hashcode.append(result.request_list()[i].paper().read_data().doc_info()[1])
		metadata.append(result.request_list()[i].paper().read_data().metadata())
		sender.append(result.request_list()[i].sender().address)
		inviteAddr.append(result.request_list()[i].address)
		
	return render_template("查看所有收到的邀請頁面.html",Address=result.infomation()['owner'],accountAddr=address,p=p,link=link,hashcode=hashcode,metadata=metadata,sender=sender,inviteAddr=inviteAddr)

@app.route("/<address>/requests",methods=["POST"])
def requests(address):	
	try:
		a=User(result.infomation()['owner'],request.form["password"])
		result.invites_list()[i].cancel_from()
		return redirect(url_for("transactions"))
	except:	
		return redirect(url_for("invitesPage",address=address))

@app.route("/<address>/requests/<inviteAddr>",methods=["GET"])
def reviewPage(address,inviteAddr):
	p=len(result.request_list())-1;
	for i in range(p):
		if inviteAddr==result.request_list()[i].address:
			paperAddr=result.request_list()[i].paper().address
			sender=result.request_list()[i].sender().address
	return render_template("審查頁面.html",Address=result.infomation()['owner'],accountAddr=address,paperAddr=paperAddr,sender=sender)
@app.route("/<address>/requests/<inviteAddr>",methods=["POST"])
def review(address,inviteAddr):

if __name__=="__main__":	
	app.run(debug=True)