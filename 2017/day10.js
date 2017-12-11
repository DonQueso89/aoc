let fs = require("fs");


let getSubarray = function(start, len, arr) {
    var result = new Array();
    var end = (start + len) % arr.length;
    if (end <= start) {
        // Wrap around
        result.push(...arr.slice(start, arr.length));
        result.push(...arr.slice(0, end));
        return result
    }
    result.push(...arr.slice(start, end));
    return result
}


let substituteArray = function(start, replacement, original) {
    var result = new Array();
    var end = (start + replacement.length) % original.length;
    var delta = end - start;
    if (delta == 0) {
        result.push(...replacement.slice(replacement.length - end, replacement.length));
        result.push(...replacement.slice(0, replacement.length - end));
    } else if (delta > 0){
        result.push(...original.slice(0, start));
        result.push(...replacement);
        result.push(...original.slice(start + replacement.length, original.length));
    } else {
        result.push(...replacement.slice(replacement.length - end, replacement.length));
        result.push(...original.slice(end, start));
        result.push(...replacement.slice(0, replacement.length - end));
    }
    return result;
}


let partOne = function(input, listSize, rounds) {
    var result = Array.apply(null, Array(listSize)).map((_, i) => i);
    var cursor = 0;
    var i, j;  // i for cycling, j for skipsize
    for (i = 0, j = 0; j < input.length * rounds; i = (i + 1) % input.length, j++) {
        var currLen = input[i];
        if (currLen > 0) { // Do something when there's something to do
            var subArr = getSubarray(cursor, currLen, result).reverse();
            result = substituteArray(cursor, subArr, result);
        }
        cursor = (cursor + (currLen + j)) % result.length;
    }
    return result;
}


let convertToASCII = function(str) {
    var result = Array.from(str).map((x) => x.charCodeAt(0));
    result.push(...[17, 31, 73, 47, 23]);
    return result;
}


let convertToDenseHash = function(arr) {
    let result = [];
    for (var i = 0; i < arr.length; i+=16) {
        result.push(eval(arr.slice(i, i + 16).join('^')));
    }
    return result;

}


let partTwo = function(inputString) {
    var result = convertToASCII(inputString);
    result = partOne(result, 256, 64); // get the sparse hash
    result = convertToDenseHash(result).map((x) => x < 16 ? '0' + x.toString(16) : x.toString(16)).join('');    
    return result;
}


var data = fs.readFileSync('inp10.txt').toString().split(',').map((x) => Number(x));
let result = partOne(data, 256, 1);
console.log("P1: " + result[0] * result[1]);

data = ['', 'AoC 2017', '1,2,3', '1,2,4'];
data.push(fs.readFileSync('inp10.txt').toString());
data.map((x) => console.log('P2: ' + x + ': ' + partTwo(x)))

