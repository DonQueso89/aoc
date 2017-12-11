let fs = require("fs");

let partOne = function(d) {
    c = 0; i = 0;
    while (0 <= i && i < d.length) {i += d[i]++; c ++;}
    console.log('P1: ' + c);
}

let partTwo = function(d) {
    c = 0; i = 0;
    while (0 <= i && i < d.length) {
        var sign = d[i] > 2 ? -1 : 1;
        d[i] += sign;
        i += (d[i] + -1 * sign); 
        c++;
    }
    console.log('P2: ' + c);
}


var data = [fs.readFileSync("inp5.txt").toString().split("\n").map(Number)];
data.push([0, 3, 0, 1, -3]);

//data.map(partOne);
data.map(partTwo);
