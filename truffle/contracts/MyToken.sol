pragma solidity ^0.6.2;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract MyToken is ERC20 {
    constructor() public ERC20("Start2Token", "S2T"){
        _mint(msg.sender, 1000);
    }
}
