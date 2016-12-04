pragma solidity ^0.4.6;

contract Paper{
	struct Info{
		string link;
		string hash_code;
		uint upload_at;
	}
	address belong_to;
	Info doc_info;
	string metadata;
	mapping(address => uint) invites;
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
		if(i.get_reviewer() == belong_to){
			throw;
		}
		if(i.get_paper() != address(this)){
			throw;
		}
		invites[msg.sender] = now;
	}
	function add_review() only_exist{
		reviews.push(msg.sender);
	}
}
contract InviteReview{
	enum State{ Init, Ready, Close }
	struct Review{
		string comment;
		bool accept;
		uint timestamp;
	}
	address reviewer;
	address sender;
	address paper;
	address close_from;
	Review this_review;
	uint value;
	State state;
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
	function get_reviewer() returns(address){
		return reviewer;
	}
	function get_sender() returns(address){
		return sender;
	}
	function get_paper() returns(address){
		return paper;
	}
	function InviteReview(address r, address p){
		if(msg.sender == r){
			throw;
		}
		sender = Account(msg.sender);
		paper = p;
		reviewer = r;
		value = 0;
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
		if(!sender.send(this.balance)){
			throw;
		}
		close_from = msg.sender;
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
	address organization;
	address owner;
	string metadata;
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
	function upload_paper(string link, string hash_code, string meta) only_owner returns(address){
		Paper p = new Paper(link, hash_code, meta);
		papers.push(p);
		return p;
	}
	function invite_review(address reviewer, address paper) only_owner payable returns(address){
		InviteReview i = new InviteReview(reviewer, paper);
		invites.push(i);
		i.push_money.value(msg.value)();		
		return i;
	}
	function notice_reviewer(address i) only_owner{
		InviteReview(i).connecting();
	}
	function append_request(){
		if(InviteReview(msg.sender).get_reviewer() != address(this)){
			throw;
		}
		requests.push(msg.sender);
	}
	function cancel_invite(address i) only_owner{
		InviteReview(i).cancel();
	}
	function done_review(address i, bool status, string comment) only_owner{
		InviteReview(i).done(status, comment);
	}
	function payable_port() payable{
	}
	function receive_money() only_owner{
		if(!owner.send(this.balance)){
			throw;
		}
	}
}
contract VirtualOrganization{
	mapping(address => address) account_map;
	function my_account() returns(address){
		address a = account_map[msg.sender];
		if(a != 0){
			return a;
		}
		a = new Account(msg.sender);
		account_map[msg.sender] = a;
		return a;
	}
}