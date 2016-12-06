pragma solidity ^0.4.6;

contract Paper{
	struct Info{
		string link;
		string hash_code;
		uint upload_at;
	}
	address public belong_to;
	Info public doc_info;
	string public metadata;
	mapping(address => uint) public invites;
	address[] reviews;
	modifier only_exist(){
		if(invites[msg.sender] == 0) throw;
		_;
	}
	function Paper(string link,string hash_code,string meta){
		belong_to = msg.sender;
		doc_info.link = link;
		doc_info.hash_code = hash_code;
		doc_info.upload_at = now;
		metadata = meta;
	}
	function add_invite(){
		InviteReview i = InviteReview(msg.sender);
		if(i.reviewer() == belong_to){
			throw;
		}
		if(i.paper() != address(this)){
			throw;
		}
		invites[msg.sender] = now;
	}
	function add_review() only_exist{
		reviews.push(msg.sender);
	}
	function list_all_reviews() returns(address[]){
		return reviews;
	}
}
contract InviteReview{
	enum State{ Init, Ready, Close }
	struct Review{
		string comment;
		bool accept;
		uint timestamp;
	}
	address public reviewer;
	address public sender;
	address public paper;
	string public cancel_from;
	Review public this_review;
	uint public value;
	State public state;
	modifier inState(State s){
		if(state != s) throw;
		_;
	}
	modifier only_sender(){
		if(msg.sender != sender) throw;
		_;
	}
	modifier only_reviewer(){
		if(msg.sender != reviewer) throw;
		_;
	}
	modifier only_sender_or_reviewer(){
		if(msg.sender != sender && msg.sender != reviewer) throw;
		_;
	}
	function InviteReview(address r, address p){
		if(msg.sender == r){
			throw;
		}
		sender = Account(msg.sender);
		paper = p;
		reviewer = r;
		value = 0;
		cancel_from = '';
		state = State.Init;
	}
	function push_money() only_sender inState(State.Init) payable{
		value += msg.value;
	}
	function connecting() only_sender inState(State.Init){
		Account(reviewer).append_request();
		Paper(paper).add_invite();
		state = State.Ready;
	}
	function cancel() only_sender_or_reviewer{
		if(state != State.Init && state != State.Ready){
			throw;
		}
		Account(sender).payable_port.value(this.balance)();
		if(msg.sender == sender){
			cancel_from = 'sender';
		}
		else{
			cancel_from = 'reviewer';
		}
		state = State.Close;
	}
	function done(bool a, string c) only_reviewer inState(State.Ready){
		this_review.accept = a;
		this_review.comment = c;
		this_review.timestamp = now;
		Paper(paper).add_review();
		Account(reviewer).payable_port.value(this.balance)();
		state = State.Close;
	}
}

contract Account{
	address public organization;
	address public owner;
	string public metadata;
	address[] papers;
	address[] invites;
	address[] requests;
	modifier only_owner(){
		if(msg.sender != owner) throw;
		_;
	}
	function Account(address a){
		organization = msg.sender;
		owner = a;
	}
	function upload_paper(string link, string hash_code, string meta) only_owner{
		Paper p = new Paper(link, hash_code, meta);
		papers.push(p);
	}
	function list_all_papers() returns(address[]){
		return papers;
	}
	function invite_review(address reviewer, address paper) only_owner payable{
		InviteReview i = new InviteReview(reviewer, paper);
		invites.push(i);
		i.push_money.value(msg.value)();		
	}
	function notice_reviewer(address i) only_owner{
		InviteReview(i).connecting();
	}
	function list_all_invites() returns(address[]){
		return invites;
	}
	function list_all_requests() returns(address[]){
		return requests;
	}
	function cancel_invite(address i) only_owner{
		InviteReview(i).cancel();
	}
	function done_review(address i, bool status, string comment) only_owner{
		InviteReview(i).done(status, comment);
	}
	function receive_money() only_owner{
		if(!owner.send(this.balance)){
			throw;
		}
	}
	function show_balance() returns(uint){
		return this.balance;
	}
	function payable_port() payable{
	}
	function append_request(){
		if(InviteReview(msg.sender).reviewer() != address(this)){
			throw;
		}
		requests.push(msg.sender);
	}
}
contract VirtualOrganization{
	mapping(address => address) public account_map;
	address[] accounts;
	function create_account(){
		address a = account_map[msg.sender];
		if(a != 0){
			throw;
		}
		a = new Account(msg.sender);
		accounts.push(a);
		account_map[msg.sender] = a;
	}
	function list_all_account() returns(address[]){
		return accounts;
	}
}