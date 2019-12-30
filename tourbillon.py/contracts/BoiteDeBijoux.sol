pragma solidity ^0.6.0;

contract BoiteDeBijoux {
    address private owner;
    mapping(address => mapping(string => string)) boite;
    mapping(address => uint) ledger;

    constructor () public {
        owner = msg.sender;
    }

    function saveMyTreasure(address addr, string memory digest, string memory sign) public returns (uint){
        require(addr != address(0));

        boite[addr][digest] = sign;
        ledger[addr] += 1;

        return ledger[addr];
    }
}
