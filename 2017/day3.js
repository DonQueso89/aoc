var fs = require("fs");
var np = require("numjs");

let multiplesOfEight = Array.from(new Array(1000).keys(), (x) => x == 0 ? 1 : x * 8)
let nthSq = (d) => d == 1 ? 1 : multiplesOfEight.map((e, i, a) => a.slice(0, i).reduce((s, v) => s + v, 0)).slice(1, ).findIndex((elem, ind, arr) => elem >= d && d > arr[Math.abs(ind - 1)]);

let nthSum = (d) => d == 1 ? 1 : multiplesOfEight.map((e, i, a) => a.slice(0, i).reduce((s, v) => s + v, 0)).slice(1, ).find((elem, ind, arr) => elem >= d && d > arr[Math.abs(ind - 1)]);

var partOne = function(d) {
    let nthMaxDist = multiplesOfEight[nthSq(d)] / 8;
    let distFromNextSum = nthSum(d) - d;
    console.log("Part 1: " + (nthMaxDist + Math.abs(nthMaxDist - distFromNextSum % (nthMaxDist * 2))));
};


var step = function(y, x, dir) {
    // take 1 step in dir direction
    switch (dir) {
        case 'R':
            return [y, ++x];
        case 'L':
            return [y, --x];
        case 'U':
            return [--y, x];
        default:
            return [++y, x];
    }
}

var calcVal = function(y, x, dGrid) {
    let dirs = 'RULD';
    var val = 0
    let adds = [
        np.array([1, 0]),
        np.array([0, 1]),
        np.array([1, 1]),
        np.array([-1, 0]),
        np.array([0, -1]),
        np.array([-1, -1]),
        np.array([1, -1]),
        np.array([-1, 1]),
    ];
    for (var i = 0; i < 8; i++) {
        var c = np.array([y, x]).add(adds[i]);
        var ty = c.get(0)
        var tx = c.get(1)
        if ((0 <= tx < 50)  && (0 <= ty < 50)) {
            val += dGrid.get(ty, tx)
        }
    }
    return val;
}


var solve = function(inp) {
    // Incr by 1 every two iterations
    var curVal = 1;
    let dGrid = np.zeros([50, 50])
    var x = Number(Math.floor(dGrid.size ** .5 / 2));
    var y = x;
    let nSteps = 1;
    let dirs = 'RULD'
    let d = 0;
    var curDir = dirs[d];
    var newCoord;
    dGrid.set(y, x, curVal);
    while (curVal <= inp) {
        // Take n steps in direction
        for (var i = 0; i < nSteps; i++) {
            newCoord = step(y, x, curDir);
            x = newCoord[1];
            y = newCoord[0];
            curVal = calcVal(y, x, dGrid);
            if (curVal > inp) {
                return curVal;
            }
            dGrid.set(y, x, curVal);
        }
        // Update direction every iter
        curDir = dirs[++d % 4];
        // Update nSteps every two iters
        if (d % 2 == 0) {
            nSteps++;
        }
    }
}


var partTwo = function(inp) {
    let curVal = solve(inp);
    console.log("Part 2: " + curVal);
}


data = [1, 12, 23, 1024, 10000];
let inp = Number(fs.readFileSync("inp3.txt").toString());
data.push(inp);
data.map(x => partOne(x));
//partTwo(inp);
