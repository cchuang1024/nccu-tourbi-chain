pragma solidity ^0.6.0;
// pragma experimental ABIEncoderV2;

contract Tourbillon {
    struct TimestampAuthorization {
        string timestamp;
        string signature;
    }

    struct Treasure {
        string myDigest;
        string mySign;
    }

    address private owner;
    string private ownerPublicKey;
    string private tourbillonAPIURL;

    mapping(address => mapping(uint => Treasure)) private myArchive;
    mapping(address => mapping(uint => TimestampAuthorization)) private tsArchive;
    mapping(address => uint) private mySerial;

    event WhatTimeIsIt(address myAddr, uint serial, string digest, string sign);

    constructor (string memory _ownerPublicKey, string memory _tourbillonAPIURL) public {
        owner = msg.sender;
        ownerPublicKey = _ownerPublicKey;
        tourbillonAPIURL = _tourbillonAPIURL;
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function saveMyTreasure(address addr, string memory digest, string memory sign) public returns (uint){
        require(addr != address(0));

        uint serial = mySerial[addr] + 1;

        myArchive[addr][serial] = Treasure(digest, sign);
        mySerial[addr] = serial;

        emit WhatTimeIsIt(addr, serial, digest, sign);

        return serial;
    }

    function timeIsIt(string memory timestamp, string memory signature, address myAddr, uint serial) public {
        require(myAddr != address(0));
        require(serial <= mySerial[myAddr]);

        tsArchive[myAddr][serial] = TimestampAuthorization(timestamp, signature);
    }

    function checkMySerial(address addr) public view returns (uint) {
        require(addr != address(0));
        return mySerial[addr];
    }

    function checkMyTime(address myAddr, uint serial) public view returns (string memory, string memory) {
        require(myAddr != address(0));
        require(serial <= mySerial[myAddr]);

        return (tsArchive[myAddr][serial].timestamp, tsArchive[myAddr][serial].signature);
    }

    function checkMyTreasure(address addr, uint serial) public view returns (string memory, string memory) {
        require(addr != address(0));
        require(serial <= mySerial[addr]);

        return (myArchive[addr][serial].myDigest, myArchive[addr][serial].mySign);
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
}
