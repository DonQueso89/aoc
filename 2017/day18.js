var fs = require("fs");

let prepareInstructions = function(instructions) {
    instructions = instructions.replace(/snd ([\-a-z0-9]+)/g, 'snd = $1;');
    instructions = instructions.replace(/set ([\-a-z0-9]+) ([\-a-z0-9]+)/g, '$1 = $2;');
    instructions = instructions.replace(/add ([\-a-z0-9]+) ([\-a-z0-9]+)/g, '$1 ? $1 += $2 : $1 = $2;');
    instructions = instructions.replace(/mul ([\-a-z0-9]+) ([\-a-z0-9]+)/g, '$1 ? $1 *= $2 : $1 = 0;');
    instructions = instructions.replace(/mod ([\-a-z0-9]+) ([\-a-z0-9]+)/g, '$1 ? $1 %= $2 : $1 = 0;');
    instructions = instructions.replace(/rcv ([\-a-z0-9]+)/g, '$1 != 0 ? stop = true : undefined;');
    instructions = instructions.replace(/jgz ([\-a-z0-9]+) ([\-0-9a-z]+)/g, '$1 > 0 ? instructionPointer += ($2 - 1) : undefined;')
    return instructions; 
}

function partOne(instructions) {
    var instructionPointer = 0; var snd; var stop = false;
    var letters = 'abcdefghijklmnopqrstuvwxyz';
    for (var it = 0; it < 26; it++) { eval('var ' + letters[it] + ';') };
    instructions = prepareInstructions(instructions).split('\n');
    while (true) {
        eval(instructions[instructionPointer]);
        instructionPointer++;
        if (stop) {
            console.log('P1: ' + snd);
            break;
        }
        if (instructionPointer >= instructions.length || instructionPointer < 0) {
            break; 
        }
    }
};

function partTwo(data) {
};

var instructions = fs.readFileSync("inp18.txt").toString();
partOne(instructions);


