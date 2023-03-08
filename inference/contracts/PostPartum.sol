// SPDX-License-Identifier: MIT
pragma solidity >=0.8.4;
// import "hardhat/console.sol";
import "./LilypadEvents.sol";
import "./LilypadCallerInterface.sol";

/**
    @notice An experimental contract for POC work to call Bacalhau jobs from FVM smart contracts
*/

contract PostPartumCaller is LilypadCallerInterface {
    LilypadEvents public bridge;

    struct Results {
        address caller;
        string prompt;
        string standardOutput;
    }

    Results[] public result;
    mapping(uint256 => string) prompts;

    event NewResult(Results image);

    constructor(address bridgeContract) {
        console.log("Deploying StableDiffusion contract");
        setLPEventsAddress(bridgeContract);
    }

    function setLPEventsAddress(address _eventsAddress) public {
        bridge = LilypadEvents(_eventsAddress);
    }

    string constant specStart =
        "{"
        '"Engine": "docker",'
        '"Verifier": "noop",'
        '"Publisher": "estuary",'
        '"Docker": {'
        '"Image": "hakymulla/postpartum:predict",'
        '"Entrypoint": ["python", "PostPartumInference.py"';

    string[] params = [
        "--ag",
        "--t",
        "--i",
        "--n",
        "--c",
        "--l",
        "--g",
        "--b",
        "--s"
    ];

    string constant specEnd =
        "]},"
        '"Resources": {"CPU": "1"},'
        '"Outputs": [{"Name": "outputs", "Path": "/outputs"}],'
        '"Deal": {"Concurrency": 1}'
        "}";

    function PostPartum(string[9] memory _values) external {
        // TODO: do proper json encoding, look out for quotes in _prompt
        string memory _prompt;
        uint256 i = 0;
        for (i = 0; i < _values.length; i++) {
            _prompt = string.concat(
                _prompt,
                string(
                    abi.encodePacked(
                        ",",
                        '"',
                        params[i],
                        '"',
                        ",",
                        '"',
                        _values[i],
                        '"'
                    )
                )
            );
        }
        string memory spec = string.concat(specStart, _prompt, specEnd);

        uint256 id = bridge.runBacalhauJob(
            address(this),
            spec,
            LilypadResultType.StdOut
        );
        prompts[id] = _prompt;
    }

    function allResult() public view returns (Results[] memory) {
        return result;
    }

    function lilypadFulfilled(
        address _from,
        uint256 _jobId,
        LilypadResultType _resultType,
        string calldata _result
    ) external override {
        //need some checks here that it a legitimate result
        require(_from == address(bridge)); //really not secure
        require(_resultType == LilypadResultType.StdOut);

        Results memory res = Results({
            caller: msg.sender,
            standardOutput: _result,
            prompt: prompts[_jobId]
        });
        result.push(res);
        emit NewResult(res);
        delete prompts[_jobId];
    }

    function lilypadCancelled(
        address _from,
        uint256 _jobId,
        string calldata _errorMsg
    ) external override {
        require(_from == address(bridge)); //really not secure
        console.log(_errorMsg);
        delete prompts[_jobId];
    }
}
