let fs = require("fs");

let partOneAndTwo = function(d) {
    var Register = Object();
    var maxVal = 0;
    for (var i = 0; i < d.length; i++) {
        var line = d[i];
        line = line.replace(/inc/g, '+');
        line = line.replace(/dec/g, '-');
        line = line.split(' ');
        var cond = line.slice(4, line.length);
        var key = line[0];
        var expr = line.slice(1, 3).join(' ');
        if (Register[key] == undefined) {
            Register[key] = 0;
        }
        if (Register[cond[0]] == undefined) {
            Register[cond[0]] = 0;
        }
        cond = "Register['" + cond[0] + "'] " + cond[1] + ' ' + cond[2];
        if (eval(cond)) {
            Register[key] += eval(expr);
        }
        maxVal = Math.max(...Object.values(Register), maxVal);
    }
    console.log('P1: ' + Math.max(...Object.values(Register)), 'P2: ' + maxVal);
}

var data = [];
data.push(fs.readFileSync("testinp8.txt").toString().split("\n"));
data.push(fs.readFileSync("inp8.txt").toString().split("\n"));
data.map(partOneAndTwo);
