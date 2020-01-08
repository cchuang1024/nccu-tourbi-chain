pragma solidity ^0.6.0;

contract Breguet {
    address private owner;
    address private tourbillon;

    constructor (address _tourbillon) public {
        owner = msg.sender;
        tourbillon = _tourbillon;
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function setTourbillonAddress(address _tourbillon) public onlyOwner {
        require(_tourbillon != address(0));
        tourbillon = _tourbillon;
    }

    fallback () external{
        address contractAddress = tourbillon;
        assembly {
            let ptr := mload(0x40)
            calldatacopy(ptr, 0, calldatasize())
            let result := delegatecall(gas(), contractAddress, ptr, calldatasize(), 0, 0)
            let size := returndatasize()
            returndatacopy(ptr, 0, size)

            switch result
            case 0 {revert(ptr, size)}
            default {return (ptr, size)}
        }
    }
}
