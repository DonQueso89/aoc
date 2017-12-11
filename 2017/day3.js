var fs = require("fs");

let multiplesOfEight = Array.from(new Array(1000).keys(), (x) => x == 0 ? 1 : x * 8)
let nthSq = (d) => d == 1 ? 1 : multiplesOfEight.map((e, i, a) => a.slice(0, i).reduce((s, v) => s + v, 0)).slice(1, ).findIndex((elem, ind, arr) => elem >= d && d > arr[Math.abs(ind - 1)]);

let nthSum = (d) => d == 1 ? 1 : multiplesOfEight.map((e, i, a) => a.slice(0, i).reduce((s, v) => s + v, 0)).slice(1, ).find((elem, ind, arr) => elem >= d && d > arr[Math.abs(ind - 1)]);

var partOne = function(d) {
    let nthMaxDist = multiplesOfEight[nthSq(d)] / 8;
    let distFromNextSum = nthSum(d) - d;
    console.log(nthMaxDist + Math.abs(nthMaxDist - distFromNextSum % (nthMaxDist * 2)))
};



data = [1, 12, 23, 1024];
data.push(Number(fs.readFileSync("inp3.txt").toString()));
data.map(partOne);
