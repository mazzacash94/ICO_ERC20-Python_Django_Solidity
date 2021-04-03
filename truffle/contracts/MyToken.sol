// SPDX-License-Identifier: MIT

pragma solidity ^0.6.8;

abstract contract ERC20Interface {
    function totalSupply() public virtual view returns (uint256);
    function balanceOf(address _owner) public virtual view returns (uint256 balance);
    function transfer(address _to, uint256 _value) internal virtual returns (bool success);

    function transferFrom(address _from, address _to, uint256 _value) internal virtual returns (bool success);
    function approve(address _spender, uint256 _value) internal virtual returns (bool success);
    function allowance(address _owner, address _spender) internal virtual view returns (uint256 remaining);

    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
}

contract Token is ERC20Interface{

    string public name = "Start2Token";
    string public symbol = "S2T";
    uint public decimals = 18;

    uint public supply;

    address payable public founder;

    mapping(address => uint) public balances;

    mapping(address => mapping(address => uint)) allowed;

    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);

    constructor() public {
        supply = 1000;
        founder = msg.sender;
        balances[founder] = supply;
    }

    function allowance(address _owner, address _spender) internal override view returns (uint256 remaining){
        return allowed[_owner][_spender];
    }

    function approve(address _spender, uint256 _value) internal override returns (bool success){
        require(balances[msg.sender] >= _value && _value > 0);
        allowed[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }

    function totalSupply() public override view returns (uint256){
        return supply;
    }

    function balanceOf(address _owner) public override view returns (uint256 balance){
        return balances[_owner];
    }

    function transfer(address _to, uint _value) internal override returns (bool success){
        balances[_to] += _value;
        balances[founder] -= _value;
        emit Transfer(founder, _to, _value);
        return true;
    }

    function transferFrom(address _from, address _to, uint256 _value) internal override returns (bool success){
        require(allowed[_from][_to] >= _value && balances[_from] >= _value);
        balances[_from] -= _value;
        balances[_to] += _value;
        allowed[_from][_to] -= _value;
        return true;
    }
}