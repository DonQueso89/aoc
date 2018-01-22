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

let prepareProgramInstructions = function(instructions) {
    instructions = instructions.replace(/snd ([\-a-z0-9]+)/g, 'yieldValue = [$1, null];');
    instructions = instructions.replace(/set ([\-a-z0-9]+) ([\-a-z0-9]+)/g, '$1 = $2;');
    instructions = instructions.replace(/add ([\-a-z0-9]+) ([\-a-z0-9]+)/g, '$1 += $2;');
    instructions = instructions.replace(/mul ([\-a-z0-9]+) ([\-a-z0-9]+)/g, '$1 *= $2;');
    instructions = instructions.replace(/mod ([\-a-z0-9]+) ([\-a-z0-9]+)/g, '$1 %= $2;');
    instructions = instructions.replace(/rcv ([\-a-z0-9]+)/g, 'queue.length > 0 ? $1 = queue.splice(0, 1)[0] : yieldValue = ["b", "$1 = queue.splice(0, 1)[0];"];');
    instructions = instructions.replace(/jgz ([\-a-z0-9]+) ([\-0-9a-z]+)/g, '$1 > 0 ? ip += ($2 - 1) : undefined;');
    return instructions; 
}

function* thread(queue, instructions, pid) {
    var ip = 0;
    var letters = 'abcdefghijklmnopqrstuvwxyz';
    for (var it = 0; it < 26; it++) { eval('var ' + letters[it] + ' = 0;') };
    var yieldValue = null;
    var postReceiveCallback = null;
    p = pid;
    while (true) {
        eval(instructions[ip]);
        if (yieldValue != null) { 
            toYield = yieldValue[0]; 
            postReceiveCallback = yieldValue[1];
            yield toYield; 
            yieldValue = null; 
        }
        if (postReceiveCallback != null) {
            eval(postReceiveCallback);
            postReceiveCallback = null;
        }
        ip++;
        if (ip >= instructions.length || ip < 0) {
            break; 
        }
    }
}

let scheduler = function(instructions) {
    let queue0 = [];
    let queue1 = [];
    let program0 = thread(queue0, instructions, 0);
    let program1 = thread(queue1, instructions, 1);
    var programRunning = program0;
    var queueReceiving = queue1;
    var nextAction;
    var terminated = 0;
    var blocked = 0;
    var valuesSent = 0;
    while (true) {
        nextAction = programRunning.next();
        switch(typeof nextAction.value) {
            case 'string':  // program blocks
                if (blocked == 0) {
                    programRunning = programRunning == program0 ? program1 : program0;
                    queueReceiving = queueReceiving == queue0 ? queue1 : queue0;
                    blocked++;
                } else if (blocked == 1 && queueReceiving.length > 0) { // the other program can continue
                    programRunning = programRunning == program0 ? program1 : program0;
                    queueReceiving = queueReceiving == queue0 ? queue1 : queue0;
                } else {
                    return valuesSent;
                }
                break;
            case 'number':  // program sends
                queueReceiving.push(nextAction.value);
                if (programRunning == program1) { valuesSent++; }
                break;
            case 'undefined':  // program terminates
                terminated++;
                if (terminated < 2) {
                    programRunning = programRunning == program0 ? program1 : program0;
                    queueReceiving = queueReceiving == queue0 ? queue1 : queue0;
                    break;
                }
                else {
                    return valuesSent;
                }
        }
    }
}

function partTwo(instructions) {
    instructions = prepareProgramInstructions(instructions).split('\n');
    let result = scheduler(instructions);
    console.log('P2: ' + result);
};

var instructions = fs.readFileSync("inp18.txt").toString();
partOne(instructions);
partTwo(instructions);
