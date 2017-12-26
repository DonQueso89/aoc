var fs = require("fs");

let partOne = function(moves) {
    moves = moves.split(',');
    let shortestPath = (x, y, upperLane) => Math.abs(y) + (Math.abs(x) - ((Math.abs(y) - upperLane) / 2 + (x > 0 && !upperLane && y % 2 != 0) || (x < 0 && upperLane && y % 2 == 0)));
    var x = 0;
    var y = 0;
    var upperLane = false;
    var switchLanes = (l) => !l;
    var maxDist = -1;
    for (i = 0; i < moves.length; i++) {
        var move = moves[i];
        switch(move) {
            case 'n':
                x++;
                break;
            case 's':
                x--;
                break;
            case 'ne':
                y++;
                if (upperLane) { x++ }
                upperLane = switchLanes(upperLane);
                break;
            case 'se':
                y++;
                if (!upperLane) { x-- }
                upperLane = switchLanes(upperLane);
                break;
            case 'nw':
                y--;
                if (upperLane) { x++ }
                upperLane = switchLanes(upperLane);
                break;
            case 'sw':
                y--;
                if (!upperLane) { x-- }
                upperLane = switchLanes(upperLane);
                break;
        }
        maxDist = Math.max(maxDist, shortestPath(x, y, upperLane));
    }
    console.log('P1: ' + shortestPath(x, y, upperLane) + ' P2: ' + maxDist);
}


var data = [fs.readFileSync("inp11.txt").toString()];
data.push(...['ne,ne,ne', 'ne,ne,sw,sw']);

data.map(partOne);
