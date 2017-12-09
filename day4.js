let fs = require("fs");

let partOne = function(d, s) {
    var c = 0;
    for (var i = 0; i < d.length; i++){
        var Counter = Object();
        var containsNoDuplicate = Object.values(d[i].reduce(
            function(s, v) {
                s[v] = s[v] ? s[v] + 1 : 1;
                return s;
            },
            Counter,
        )).find((x) => x > 1) === undefined;
        if (containsNoDuplicate) {
            c++;
        }
    }
    console.log(s + c);
}

let partTwo = function(d) {
    var d = d.map((x) => x.map((y) => Array.from(y).sort().join('')));
    partOne(d, 'P2: ')
}

let data = fs.readFileSync("inp4.txt").toString().split("\n").map((e) => e.split(" "));
partOne(data, 'P1: ');
partTwo(data);
