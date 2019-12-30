pragma solidity ^0.6.0;

contract Tiffany {
    address private owner;
    address private boite_de_bijoux;
    bytes private ownerPublicKey;

    constructor (address boite) public {
        owner = msg.sender;
        boite_de_bijoux = boite;
        ownerPublicKey = new bytes(64);
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function setBoiteAddress(address boite) public onlyOwner {
        require(boite != address(0));
        boite_de_bijoux = boite;
    }

    function setOwnerPublicKey(bytes memory publicKey) public onlyOwner {
        ownerPublicKey = publicKey;
    }

    function getOwnerPublicKey() public view returns (bytes memory) {
        return ownerPublicKey;
    }

    fallback () external{
        address contractAddress = boite_de_bijoux;
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
