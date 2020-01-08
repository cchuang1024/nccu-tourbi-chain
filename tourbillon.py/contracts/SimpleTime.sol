pragma solidity ^0.6.0;

contract SimpleTime {
    address private owner;
    string private timestamp;

    event WhatTimeIsIt(address requestor);

    constructor() public {
        owner = msg.sender;
    }

    function whatTimeIsIt(address requestor) public {
        emit WhatTimeIsIt(requestor);
    }

    function timeIsIt(string memory time) public {
        timestamp = time;
    }

    function getTime() public view returns (string memory) {
        return timestamp;
    }
}
