var fs = require("fs");

function partOne(data) {
    console.log(Array.from(data).reduce(function(sum, value, ind){
        if (value == data[((ind + 1) % data.length)]) {
            return sum + Number(value);
        }
        else {
            return Number(sum);
        }
    }, 0));
};

function partTwo(data) {
    console.log(Array.from(data).reduce(function(sum, value, ind){
        if (value == data[((ind + data.length / 2) % data.length)]) {
            return sum + Number(value);
        }
        else {
            return Number(sum);
        }
    }, 0));
};


var data = [];
data.push(...['1212', '1221', '123425', '123123', '12131415']);
data.push(fs.readFileSync("inp1.txt").toString());
data.map(partTwo)


