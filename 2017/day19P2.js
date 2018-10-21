var fs = require("fs");
var np = require("numjs");

function partTwo(grid) {
};



var inp = fs.readFileSync("inp19.txt").toString().split('\n').map((x) => Array.from(x))

let grid = np.zeros([inp.length, inp[0].length]);

partTwo(grid);
for (var i = 0; i < inp.length; i++) {
    var row = inp[i];
    for (var j = 0; j < row.length; j++) {
        grid.set(i, j, inp[i][j]);
    }
}
console.log(grid);
