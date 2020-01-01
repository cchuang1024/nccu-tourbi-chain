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

    mapping(address => mapping(uint => Treasure)) private myArchive;
    mapping(address => mapping(uint => TimestampAuthorization)) private tsArchive;

    mapping(address => uint) private mySerial;
    mapping(address => uint) private ledger;

    event WhatTimeIsIt(address myAddr, uint serial);

    constructor () public {
        owner = msg.sender;
    }

    function saveMyTreasure(address addr, string memory digest, string memory sign) public {
        require(addr != address(0));

        uint serial = mySerial[addr] + 1;

        myArchive[addr][serial] = Treasure(digest, sign);
        mySerial[addr] = serial;

        emit WhatTimeIsIt(addr, serial);
    }

    function checkMySerial(address addr) public view returns (uint) {
        require(addr != address(0));
        return mySerial[addr];
    }

    function checkMyTreasure(address addr, uint serial) public view returns (string memory,
                                                                             string memory,
                                                                             string memory,
                                                                             string memory) {
        require(addr != address(0));
        require(serial <= mySerial[addr]);

        return (myArchive[addr][serial].myDigest,
                myArchive[addr][serial].mySign,
                tsArchive[addr][serial].timestamp,
                tsArchive[addr][serial].signature);
    }

    function itsTime(address myAddr, uint serial, string memory timestamp, string memory signature) public {
        require(myAddr != address(0));
        require(serial <= mySerial[myAddr]);

        tsArchive[myAddr][serial] = TimestampAuthorization(timestamp, signature);
    }

    function getTime(address myAddr, uint serial) public view returns (string memory, string memory) {
        require(myAddr != address(0));
        require(serial <= mySerial[myAddr]);

        return (tsArchive[myAddr][serial].timestamp, tsArchive[myAddr][serial].signature);
    }
}
