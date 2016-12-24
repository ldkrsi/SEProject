from web3 import Web3, KeepAliveRPCProvider
import os, sys
import json
import time
import redis

get_file_path = lambda *res: os.path.normpath(os.path.join(os.getcwd(), os.path.dirname(__file__), *res))

config = json.load(open(get_file_path('','config.json'),'r'))
web3 = Web3(KeepAliveRPCProvider(host=config['host'], port=config['port']))
zero = '0x0000000000000000000000000000000000000000'

rds = redis.StrictRedis(host='localhost', port=6379, db=3)

def send_transaction_syn(t_hash,t_name):
	print(t_name)
	t, counter = None, 0
	while t is None:
		print( '\r' + str(counter), end="")
		t = web3.eth.getTransactionReceipt(t_hash)
		time.sleep(1)
		counter +=1
	print()
	print(json.dumps(t, indent=4, sort_keys=True))
	return t

def send_transaction_asyn(t_hash,t_name):
	rds.set(str(time.time()), json.dumps([False, t_hash, t_name]))

class User:
	def __init__(self, address, pwd=None):# string address, string pwd
		self.address = address
		self.pwd = pwd
		if self.pwd is not None:
			self.login()
	def login(self):
		web3.personal.unlockAccount(self.address, self.pwd)


class BaseModel:
	def __init__(self, address): # string address
		self.entity = web3.eth.contract(self.abi, code=self.code, address=address)
	#private
	def write_data(self, value=None): #int value
		if value is None:
			return self.entity.transact({'from': self.owner.address})
		return self.entity.transact({
			'from': self.owner.address,
			'value': int(value)
		})
	#private
	def read_data(self):
		return self.entity.call()
	@property
	def address(self):
		return self.entity.address

class Organization(BaseModel):
	abi = json.load(open(get_file_path('contract','VirtualOrganization.abi'),'r'))
	code = open(get_file_path('contract','VirtualOrganization.bin'),'r').read()
	def get_my_account(self,user): # User user
		a = self.find_account(user)
		if a is not None:
			return a
		self.create_account(user)
		return self.find_account(user)
	def find_account(self, user): # User user
		if user is None:
			user = defaultUser
		addr = self.read_data().account_map(user.address)
		if addr == zero:
			return None
		return Account(addr,user)
	#private
	def create_account(self,user): # User user
		token = self.entity.transact({'from': user.address}).create_account()
		send_transaction_asyn(token, "create account")
	def account_list(self):
		return self.read_data().list_all_account()


class Account(BaseModel):
	abi = json.load(open(get_file_path('contract','Account.abi'),'r'))
	code = open(get_file_path('contract','Account.bin'),'r').read()
	def __init__(self, address, user=None): #string address, User user
		super().__init__(address)
		if user is not None:
			self.owner = user
	def infomation(self):
		return {
			'organization': self.read_data().organization(),
			'owner': self.read_data().owner(),
			'metadata': self.read_data().metadata(),
		}
	def upload_paper(self, link, hash_code, meta_data): #string link, string hash_code, string meta_data
		token = self.write_data().upload_paper(link, hash_code, meta_data)
		send_transaction_asyn(token,'upload paper')
	def papers_list(self):
		return [Paper(p) for p in self.read_data().list_all_papers()]
	def invite_review(self, reviewer, paper, value): #Acount reviewer, Paper paper, int value(wei)
		token1 = self.write_data(value).invite_review(reviewer.address, paper.address)
		send_transaction_syn(token1,'make invite')
		i = self.invites_list()[-1]
		token2 = self.write_data().notice_reviewer(i.address)
		send_transaction_asyn(token2,'connect to user')
	def cancel_invite(self, i): #InviteReview i
		token = self.write_data().cancel_invite(i.address)
		send_transaction_asyn(token,'cancel invite')
	def invites_list(self):
		return [InviteReview(i) for i in self.read_data().list_all_invites()]
	def request_list(self):
		return [InviteReview(i) for i in self.read_data().list_all_requests()]
	def done_review(self, inv, accept, comment): # InviteReview inv, bool accept, string comment
		token = self.write_data().done_review(inv.address, accept, comment)
		send_transaction_asyn(token,'done review')
	def send_money_to_owner(self):
		token = self.write_data().receive_money()
		send_transaction_asyn(token,'send back money')
	def get_balance(self):
		return self.read_data().show_balance()
class Paper(BaseModel):
	abi = json.load(open(get_file_path('contract','Paper.abi'),'r'))
	code = open(get_file_path('contract','Paper.bin'),'r').read()
	def infomation(self):
		return {
			'belong to': self.belog_to(),
			'doc info': self.read_data().doc_info(),
			'metadata': self.read_data().metadata(),
			'review count': len(self.review_list())
		}
	def belog_to(self):
		return Account(self.read_data().belong_to())
	def review_list(self):
		return [InviteReview(i) for i in self.read_data().list_all_reviews()]

class InviteReview(BaseModel):
	abi = json.load(open(get_file_path('contract','InviteReview.abi'),'r'))
	code = open(get_file_path('contract','InviteReview.bin'),'r').read()
	def infomation(self):
		return {
			'review': self.read_data().this_review(),
			'value': self.read_data().value(),
			'state': self.read_data().state(),
			'reviewer': self.reviewer(),
			'sender': self.sender(),
			'paper': self.paper(),
			'cancel_from': self.cancel_from()
		}
	def reviewer(self):
		return Account(self.read_data().reviewer())
	def sender(self):
		return Account(self.read_data().sender())
	def paper(self):
		return Paper(self.read_data().paper())
	def cancel_from(self):
		return self.read_data().cancel_from()


defaultUser = User(config['account'],config['password'])
root = Organization(config['organization'])
if __name__ == '__main__':
	one = root.get_my_account(defaultUser)
	two = root.get_my_account(User('0x56a9a02403bE71a4e44F9ff42f06E379A6E2fD27', '12345678'))
	#print(User('0x56a9a02403bE71a4e44F9ff42f06E379A6E2fD27').pwd)
	print(one.infomation())
	print(one.entity.address)
	#print(two.entity.address)
	p = one.upload_paper("http://example.com","001","test")
	#test1
	#print(two.papers_list()[1].address)
#	print(two.owner.pwd)
	#print(two.read_data().list_all_requests()[0].paper.read_data().doc_info()[0])
	#print(InviteReview(two).infomation())
	k=len(two.request_list())-1
	
	link=[]
	hashcode=[]
	metadata=[]
	sender=[]
	for i in range(k):
		print(two.request_list()[i].paper().read_data().doc_info()[0])
		print(two.request_list()[i].paper().read_data().doc_info()[1])
		print(two.request_list()[i].paper().read_data().metadata())
		print(two.request_list()[i].sender().address)
	print(two.request_list())
	print(two.request_list()[0].infomation())
	#print(two.request_list()[0].belog_to().address)
	print(two.request_list()[0].address)
#	print(two.two.request_list()[0].read_data().belong_to())
	print(two.request_list()[0].paper().address)
	print(two.request_list()[0].read_data().state())

#print(two.request_list()[0])
#print(two.papers_list()[0].read_data().doc_info()[2])
	#print(two.papers_list()[0].address)
'''
	i = one.invite_review(two, one.papers_list()[0] ,'1000000')
	print(i)
	print(one.invites_list())

	#one.cancel_invite(i)
	#print(one.get_balance())
	#one.send_money_to_owner()
	#print(one.get_balance())
	
	
	
	p = None
	if len(one.papers_list()) > 0:
		p = one.papers_list()[0]
	else:
		p = one.upload_paper("http://example.com","001","test")
	print(p.read_data().metadata())
	
	
	ModelRoot.find_account(User('0x56a9a02403bE71a4e44F9ff42f06E379A6E2fD27')).papers_list()[i].read_data().metadata()
	i = one.invite_review(two, p ,'10000000000000000000')
	print(i.infomation(), i.reviewer().address, i.sender().address, i.paper().infomation())
	print(one.invites_list())
	print(two.papers_list()[0].request_list())
	
	two.done_review(i,True,'some comments')
	print(i.infomation())
	print(p.review_list()[0].infomation())
	print(two.get_balance())
	two.send_money_to_owner()
	print(two.get_balance())
	
	#test2
	p = None
	if len(two.papers_list()) > 0:
		p = two.papers_list()[0]
	else:
		p = two.upload_paper("http://example.com","000","test")
	print(p)

	i = two.invite_review(one.entity.address, p ,'10000000000000000000')
	print(i)
	print(two.invites_list())

	two.cancel_invite(i)
	print(two.get_balance())
	two.send_money_to_owner()
	print(two.get_balance())
	
	#test3
	p = None
	if len(two.papers_list()) > 0:
		p = two.papers_list()[0]
	else:
		p = two.upload_paper("http://example.com","000","test")
	print(p)

	i = two.invite_review(one, p ,'10000000000000000000')
	print(i.infomation())
	print(two.invites_list())
	one.cancel_invite(i)
	print(i.infomation())
	print(two.get_balance())
	two.send_money_to_owner()
	print(two.get_balance())
	'''
	#test4
	#print(one.papers_list()[0].review_list()[0].infomation())
