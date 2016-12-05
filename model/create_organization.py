from model import web3, send_transaction, config, defaultUser
import json

if __name__ == '__main__':
	a = json.load(open('contract/VirtualOrganization.abi','r'))
	c = open('contract/VirtualOrganization.bin','r').read()
	contract = web3.eth.contract(a,code=c)
	t_hash = contract.deploy(transaction={
		'from': defaultUser.address,
	})
	token = send_transaction(t_hash,'create organization')
	config['organization'] = token["contractAddress"]
	with open('config.json','w') as f:
		f.write(json.dumps(config, indent=4, sort_keys=True))

