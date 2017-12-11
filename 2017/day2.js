var fs = require("fs");
var partOne = function(d){
    console.log(d.reduce(function(sum, val) { 
        val.sort((a, b) => a - b);
        return (sum + (val[val.length - 1] - val[0]));
    }, 0));
}

var partTwo = function(d) {
    console.log(d.reduce(function(sum, val) {
        val.sort((a, b) => a - b);
        for (i in val) {
            let subArr = val.slice(0, i);
            for (j in subArr) {
                if (val[i] % val[j] == 0) {
                    return sum + val[i] / val[j];
                }
            }
        };
    }, 0));
}


var data = fs.readFileSync('inp2.txt').toString().split('\n').map((v) => v.split('\t')).map((w) => w.map(Number));
//partOne(data);
partTwo(data);
