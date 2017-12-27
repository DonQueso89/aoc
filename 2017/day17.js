var fs = require("fs");
let jumpSize = 316;

function partOne() {
    // brute force
    var state = [0];
    for (i = 0, v = 1; v <= 2017; v++, i = (i + jumpSize) % state.length) {
        i++;
        state = state.slice(0, i).concat(v).concat(state.slice(i, ));
    }
    console.log('P1: ' + state[state.findIndex((x) => x == 2017) + 1]);
};

function partTwo() {
    // 0 will always be at index 0
    var lastIndex = 1;
    // Calculate pos before last insert
    for (var i = 1; i <= 50000000; i++) { lastIndex = (++lastIndex + jumpSize) % i }
    // Starting from last index, calculate most recent insert at pos 1
    var valueToInsert = 50000000;
    while (lastIndex != 0) {
        lastIndex -= (jumpSize + 1);
        lastIndex = lastIndex < 0 ? valueToInsert - Math.abs(lastIndex) : lastIndex;
        valueToInsert--;
    }
    console.log('P2: ' + valueToInsert);
};

partOne();
partTwo();
