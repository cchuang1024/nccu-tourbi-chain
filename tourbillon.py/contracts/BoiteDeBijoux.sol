pragma solidity ^0.6.0;

abstract contract Tourbillon {
    function whatTimeIsIt(address myAddr) public virtual returns (uint);
    function itsTime(address myAddr, uint serial, string memory timestamp, string memory signature) public virtual;
    function getTime(address myAddr, uint serial) public virtual view returns (string memory, string memory);
}

contract BoiteDeBijoux {
    struct Treasure {
        string mySign;
        string timestamp;
        string tsSign;
    }

    address private owner;
    Tourbillon private tourbillon;

    mapping(address => uint) private ledger;
    mapping(address => mapping(string => Treasure)) private boite;

    constructor (address tourbAddr) public {
        owner = msg.sender;
        tourbillon = Tourbillon(tourbAddr);
    }

    function saveMyTreasure(address addr, string memory digest, string memory sign) public returns (uint){
        require(addr != address(0));

        uint serial = tourbillon.whatTimeIsIt(addr);
        (string memory timestamp, string memory tsSign) = tourbillon.getTime(addr, serial);

        boite[addr][digest] = Treasure(sign, timestamp, tsSign);
        ledger[addr] += 1;

        return ledger[addr];
    }

    function checkMyLedger(address addr) public view returns (uint) {
        require(addr != address(0));
        return ledger[addr];
    }

    function checkMyTreasure(address addr, string memory digest) public view returns (string memory, string memory, string memory) {
        require(addr != address(0));
        return (boite[addr][digest].mySign,
                boite[addr][digest].timestamp,
                boite[addr][digest].tsSign);
    }
}
