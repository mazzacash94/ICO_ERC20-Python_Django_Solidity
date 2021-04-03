// SPDX-License-Identifier: MIT

pragma solidity ^0.6.8;

import "./MyToken.sol";

contract Ico is Token{

    uint public tokenPrice = 1 ether;
    uint public maxInvestment = 100 ether;
    uint public minInvestment = 1 ether;
    uint public startDate;
    uint public endDate;
    enum State {beforeStart, Running, afterEnd, Stopped}
    State public icoState;

    modifier onlyAdmin(){
        require(msg.sender == founder);
        _;
    }

    event Invest(address invester, uint value, uint tokens);

    constructor(uint daysLength) public {
        icoState = State.beforeStart;
        startDate = now;
        endDate = now + daysLength*86400;
    }

    function checkFinish() private{
        if (now > endDate){
            icoState = State.afterEnd;
            burn();
        }
    }

    function start() public onlyAdmin{
        checkFinish();
        require(icoState == State.beforeStart);
        icoState = State.Running;
    }

    function end() public onlyAdmin{
        checkFinish();
        require(icoState == State.Running);
        icoState = State.afterEnd;
        burn();
    }

    function resume() public onlyAdmin{
        checkFinish();
        require(icoState == State.Stopped);
        icoState = State.Running;
    }

    function stop() public onlyAdmin{
        checkFinish();
        require(icoState == State.Running);
        icoState = State.Stopped;
    }

    function invest() payable public returns(bool){
        checkFinish();
        uint tokens = msg.value / tokenPrice;
        require(icoState == State.Running && msg.value >= minInvestment && msg.value <= maxInvestment && balances[founder] >= tokens && now < endDate);
        founder.transfer(msg.value);
        emit Invest(msg.sender, msg.value, tokens);
        super.transfer(msg.sender, tokens);
        return true;
    }

    receive() payable external{
        checkFinish();
        require(icoState == State.Running);
        invest();
    }

    function transferToken(address _to, uint _value) public{
        require(icoState == State.afterEnd);
        super.approve(_to, _value);
        super.transferFrom(msg.sender, _to, _value);
    }

    function burn() internal returns(bool){
        require(icoState == State.afterEnd);
        balances[founder] = 0;
    }
}