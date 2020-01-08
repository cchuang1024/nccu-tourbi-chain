pragma solidity ^0.6.0;

contract Breguet {
    address private owner;
    address private tourbillon;
    string private ownerPublicKey;
    string private tourbillonAPIURL;

    constructor (address _tourbillon, string memory _ownerPublicKey, string memory _tourbillonAPIURL) public {
        owner = msg.sender;
        tourbillon = _tourbillon;
        ownerPublicKey = _ownerPublicKey;
        tourbillonAPIURL = _tourbillonAPIURL;
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function setTourbillonAddress(address _tourbillon) public onlyOwner {
        require(_tourbillon != address(0));
        tourbillon = _tourbillon;
    }

    function setOwnerPublicKey(string memory _ownerPublicKey) public onlyOwner {
        ownerPublicKey = _ownerPublicKey;
    }

    function setTourbillonAPIURL(string memory _tourbillonAPIURL) public onlyOwner {
        tourbillonAPIURL = _tourbillonAPIURL;
    }

    function getOwnerPublicKey() public view returns (string memory) {
        return ownerPublicKey;
    }

    function getTourbillonAPIURL() public view returns (string memory) {
        return tourbillonAPIURL;
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
