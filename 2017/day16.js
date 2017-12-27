var fs = require("fs");

let unshift = function(config, n) { 
    n = n % config.length;
    let result = config.slice(config.length - n, );
    result.push(...config.slice(0, config.length - n));
    return result;
}

let exchange = function(config, x1, x2) {
    let s1 = config[x1];
    let s2 = config[x2];
    s1 = s1 + s2;
    s2 = s1 - s2;
    s1 = s1 - s2;
    config[x1] = s1;
    config[x2] = s2;
    return config;
}

let findAscii = (a, n) => a.findIndex((x) => String.fromCharCode(x) == n);

let partner = function(config, n1, n2) {
    let x1 = findAscii(config, n1); let x2 = findAscii(config, n2);
    return exchange(config, x1, x2);  
}

let doTheDance = function(config, moves) {
    for (var i = 0; i < moves.length; i++) { eval(moves[i]); }
    return config;
}

let prepareDance = function(moves){
    // Replace moves with func calls
    moves = moves.replace(/([,]*)s(\d+)([,]*)/g, '$1config = unshift(config, $2);$3')
    moves = moves.replace(/([,]*)x(\d+)\/(\d+)([,]*)/g, '$1config = exchange(config, $2, $3);$4')
    moves = moves.replace(/([,]*)p([a-p]{1})\/([a-p]{1})([,]*)/g, '$1config = partner(config, "$2", "$3");$4')
    moves = moves.split(';,');
    return moves;
}

function partOne(moves) {
    var config = [];
    for (var i = 97; i < 97 + 16; i++) { 
        config.push(i); // ascii for swapping with arithmetic
    }
    let dance = prepareDance(moves);
    config = doTheDance(config, dance);
    console.log('P1: ' + config.map((x) => String.fromCharCode(x)).join(''));
};

function partTwo(moves) {
    var config = [];
    var initialConfig = [];
    var iterations = 0;
    let s = JSON.stringify;
    for (var i = 97; i < 97 + 16; i++) { 
        config.push(i); // ascii for swapping with arithmetic
        initialConfig.push(i);
    }
    let dance = prepareDance(moves);
    while (iterations < 1000000000) {
        config = doTheDance(config, dance);
        iterations++;
        if (s(config) == s(initialConfig)) {
            iterations = 1000000000 - 1000000000 % iterations;
        } 
    }
    console.log('P2: ' + config.map((x) => String.fromCharCode(x)).join(''))
};


var moves = fs.readFileSync("inp16.txt").toString().trim();
partTwo(moves);
