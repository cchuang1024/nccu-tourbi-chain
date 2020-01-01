pragma solidity ^0.6.0;
// pragma experimental ABIEncoderV2;

contract Tourbillon {
    struct TimestampAuthorization {
        string timestamp;
        string signature;
    }

    address private owner;
    mapping(address => mapping(uint => TimestampAuthorization)) myTimestampAuth;
    mapping(address => uint) mySerial;

    event WhatTimeIsIt(address myAddr, uint serial);

    constructor () public {
        owner = msg.sender;
    }

    function whatTimeIsIt(address myAddr) public returns (uint) {
        require(myAddr != address(0));

        uint serial = mySerial[myAddr] + 1;
        emit WhatTimeIsIt(myAddr, serial);
        return serial;
    }

    function itsTime(address myAddr, uint serial, string memory timestamp, string memory signature) public {
        require(myAddr != address(0));
        require(serial > mySerial[myAddr]);

        mySerial[myAddr] = serial;
        myTimestampAuth[myAddr][serial] = TimestampAuthorization(timestamp, signature);
    }

    function getTime(address myAddr, uint serial) public view returns (string memory, string memory) {
        require(myAddr != address(0));
        require(serial <= mySerial[myAddr]);

        return (myTimestampAuth[myAddr][serial].timestamp, myTimestampAuth[myAddr][serial].signature);
    }
}
