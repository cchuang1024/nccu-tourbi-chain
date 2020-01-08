pragma solidity ^0.6.0;
// pragma experimental ABIEncoderV2;

abstract contract Tourbillon {
    function saveMyTreasure(address addr, string memory digest, string memory sign) public virtual returns (uint);
    function timeIsIt(string memory timestamp, string memory signature, address myAddr, uint serial) public virtual;
    function checkMySerial(address addr) public virtual view returns (uint);
    function checkMyTime(address myAddr, uint serial) public virtual view returns (string memory, string memory);
    function checkMyTreasure(address addr, uint serial) public virtual view returns (string memory, string memory);
    function setOwnerPublicKey(string memory _ownerPublicKey) public virtual;
    function setTourbillonAPIURL(string memory _tourbillonAPIURL) public virtual;
    function getOwnerPublicKey() public virtual view returns (string memory);
    function getTourbillonAPIURL() public virtual view returns (string memory);
}

contract Breguet is Tourbillon{
    Tourbillon private tourbillon;
    address private owner;

    constructor (address _tourbillon) public {
        owner = msg.sender;
        tourbillon = Tourbillon(_tourbillon);
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function saveMyTreasure(address addr, string memory digest, string memory sign) public override returns (uint){
        return tourbillon.saveMyTreasure(addr, digest, sign);
    }

    function timeIsIt(string memory timestamp, string memory signature, address myAddr, uint serial) public override{
        tourbillon.timeIsIt(timestamp, signature, myAddr, serial);
    }

    function checkMySerial(address addr) public override view returns (uint){
        return tourbillon.checkMySerial(addr);
    }

    function checkMyTime(address myAddr, uint serial) public override view returns (string memory, string memory){
        return tourbillon.checkMyTime(myAddr, serial);
    }

    function checkMyTreasure(address addr, uint serial) public override view returns (string memory, string memory){
        return tourbillon.checkMyTreasure(addr, serial);
    }

    function setOwnerPublicKey(string memory _ownerPublicKey) public override onlyOwner{
        tourbillon.setOwnerPublicKey(_ownerPublicKey);
    }

    function setTourbillonAPIURL(string memory _tourbillonAPIURL) public override onlyOwner{
        tourbillon.setTourbillonAPIURL(_tourbillonAPIURL);
    }

    function getOwnerPublicKey() public override view returns (string memory){
        return tourbillon.getOwnerPublicKey();
    }

    function getTourbillonAPIURL() public override view returns (string memory){
        return tourbillon.getTourbillonAPIURL();
    }
}
