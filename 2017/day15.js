var fs = require("fs");

function partOne(data) {
    var data = data.map((x) => x.split(' '));
    var A = Number(data[0][4]); var B = Number(data[1][4]);
    const factorA = 16807; const factorB = 48271;
    const mod = 2147483647;
    var matchCount = 0;
    for (var i = 0; i < 40000000; i++) {
        A = A * factorA % mod; B = B * factorB % mod;
        binA = A.toString(2); binB = B.toString(2);
        if (binA.slice(binA.length - 16, ) == binB.slice(binB.length - 16)) {
            matchCount++; 
        }
    }
    console.log('P1: ' + matchCount);
};

function partTwo(data) {
    var data = data.map((x) => x.split(' '));
    var A = Number(data[0][4]); var B = Number(data[1][4]);
    const factorA = 16807; const factorB = 48271;
    const mod = 2147483647;
    var matchCount = 0;
    var Anumbers = [];
    var Bnumbers = [];
    while (Anumbers.length < 5000000) {
        A = A * factorA % mod;
        if (A % 4 == 0) {
            Anumbers.push(A);
        }
    }
    while (Bnumbers.length < 5000000) {
        B = B * factorB % mod;
        if (B % 8 == 0) {
            Bnumbers.push(B);
        }
    }
    for (var j = 0; j < Anumbers.length; j++) {
        A = Anumbers[j]; B = Bnumbers[j];
        binA = A.toString(2); binB = B.toString(2);
        if (binA.slice(binA.length - 16, ) == binB.slice(binB.length - 16)) {
            matchCount++; 
        }
    }
    console.log('P1: ' + matchCount);
};


var data = fs.readFileSync("inp15.txt").toString().split('\n');
partTwo(data);


