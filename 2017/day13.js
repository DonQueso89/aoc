var fs = require("fs");

let getSeverity = function(fireWall) {
    return fireWall.reduce(function(sum, layer) {
        var depth = layer[0];
        var range = layer[1];
        var interval = (range - 1) * 2; // ps to return to initial state
        return depth % interval == 0 ? sum + depth * range : sum;
    }, 0);
}

function partOne(fireWall) {
    console.log('P1: ' + getSeverity(fireWall, 0));
};

function partTwo(fireWall) {
    var severity;
    // Each extra delayed picosecond means a depth of +1
    for (var delay = 0; delay < Infinity; delay++) {
        severity = getSeverity(fireWall);
        fireWall = fireWall.map((x) => [x[0] + 1, x[1]]);
        if (severity == 0) {
            break;
        }
    }
    console.log('P2: ' + delay);
};


var data = fs.readFileSync("inp13.txt").toString().trim().split('\n').map((x) => x.split(':').map(Number));
//partOne(data);
partTwo(data);
