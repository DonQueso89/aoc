let fs = require("fs");


var partOne = function(stream) {
    var score = 0;
    var currentDepth = 0;
    var garbageMode = false;

    for (var i = 0; i < stream.length; i++) {
        var char = stream[i];
        if (garbageMode) {
            if (char == '!') {
                i++;
            } else if (char == '>') {
                garbageMode = false;
            }
            continue;
        }
        // No garbageMode
        if (char == '<') {
            garbageMode = true;
        } else if (char == '{'){
            currentDepth++;
        } else if (char == '}') {
            score += currentDepth--;
        }
    }
    console.log(score);
}


var partTwo = function(stream) {

}


var data = [
    '{{{},{},{{}}}}',
    '{{<ab>},{<ab>},{<ab>},{<ab>}}',
    '{{<!!>},{<!!>},{<!!>},{<!!>}}',
    '{{<a!>},{<a!>},{<a!>},{<ab>}}',
]
data.push(fs.readFileSync('inp9.txt').toString());
data.map(partOne);
