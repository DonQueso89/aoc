let fs = require("fs");

let partOne = function(d) {
    var Counter = Object();
    while (!Object.values(Counter).includes(2)) {
        k = d.join(' ');
        Counter[k] = Counter[k] == undefined ? 1 : Counter[k] + 1;
        var i = d.findIndex((x) => x == Math.max(...d));
        var v = d[i];
        d[i] = 0;
        while (v > 0) {
            i = (i + 1) % d.length;
            d[i]++;
            v--;
        }
    }
    console.log(Object.values(Counter).reduce((s, v) => s + v) - 1);
}

let partTwo = function(d) {
    var Counter = Object();
    var iter = 0;
    var k = d.join(' ');
    if (Counter[k] == undefined) { 
        Counter[k] = [iter];
    } else {
        Counter[k].push(iter);
    }
    while (!Object.values(Counter).find((x) => x.length == 2)) {
        var i = d.findIndex((x) => x == Math.max(...d));
        var v = d[i];
        d[i] = 0;
        while (v > 0) {
            i = (i + 1) % d.length;
            d[i]++;
            v--;
        }
        k = d.join(' ');
        iter++;
        if (Counter[k] == undefined) { 
            Counter[k] = [iter];
        } else {
            Counter[k].push(iter);
        }
    }
    console.log(Counter);
    console.log(Counter[k][Counter[k].length - 1] - Counter[k][0]);
}

var data = [];
data.push([0, 2, 7, 0]);
data.push(fs.readFileSync("inp6.txt").toString().split("\t").map(Number));
//data.map(partOne);
data.map(partTwo);
