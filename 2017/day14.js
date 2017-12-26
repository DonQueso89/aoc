var getKnotHash = require('./day10');
var fs = require("fs");


let toBinaryString = function(hexString) {
    var result = '';
    for (var i = 0; i < hexString.length; i++) {
        var hex = hexString[i];
        var dec = Number.parseInt(hex, 16);
        var paddingZeroes = dec >= 8 ? '' : dec >= 4 ? '0' : dec >= 2 ? '00' : '000';
        result += (paddingZeroes + dec.toString(2));
    }
    return result;
}

let sum = (x) => x.reduce((s, v) => s + v);

let getGrid = function(key) {
    var result = [];
    for (var i = 0; i < 128; i++) {
        var knotHash = getKnotHash(key + '-' + i);
        var binaryHash = toBinaryString(knotHash);
        result.push(Array.from(binaryHash).map(Number));
    }
    return result;
}

function partOne(key) {
    let result = sum(getGrid(key).map(sum));
    console.log('P1: ' + result);
};

// Return all used adjacent coordinates
let adjacents = function(x, y, binaryGrid) {
    let down = [x + 1, y];
    let up = [x - 1, y];
    let left = [x, y - 1];
    let right = [x, y + 1];
    return [down, up, left, right].filter((x) => binaryGrid[x[0]] != undefined && binaryGrid[x[0]][x[1]] == 1);

}

// Replaces a region of 1's with zeroes recursively
let replaceRegion = function(x, y, binaryGrid) {
    binaryGrid[x][y] = 0;
    var adjacentCoordinates = adjacents(x, y, binaryGrid);
    adjacentCoordinates.forEach((c) => replaceRegion(c[0], c[1], binaryGrid));
}

function partTwo(key) {
    let binaryGrid = getGrid(key);
    var nGroups = 0;
    for (var x = 0; x < binaryGrid.length; x++) {
        for (var y = 0; y < binaryGrid.length; y++) {
            if (binaryGrid[x][y] == 1) {
                nGroups++;
                replaceRegion(x, y, binaryGrid);
            }
        }
    }
    console.log('P2: ' + nGroups)
};

var key = 'oundnydw';
//partOne(key);
partTwo(key);
