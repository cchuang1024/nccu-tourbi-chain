pragma solidity ^0.4.0;

contract Tourbillon {
    address private owner;
    timestamp_authorize private _timestamp;

    struct timestamp_authorize {
        uint timestamp;
        bytes signature;
    }

    event WhatTimeIsIt(address sender);
    event ItsTime(address sender, timestamp_authorize tsa);

    constructor () {
        owner = msg.sender;
        _timestamp = timestamp_authorize(0, hex'00');
    }

    function whatTimeIsIt() public {
        emit WhatTimeIsIt(msg.sender);
    }

    function itsTime(uint timestamp, bytes signature) public {
        _timestamp = timestamp_authorize(timestamp, signature);
        emit ItsTime(msg.sender, _timestamp);
    }

    function getTime() public returns (timestamp_authorize) {
        return _timestamp;
    }
}
