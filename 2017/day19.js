var fs = require("fs");

let letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';

let nextCoordinate = {
    'U': (c) => [-1 + c[0], 0 + c[1]],
    'D': (c) => [1 + c[0], 0 + c[1]],
    'L': (c) => [0 + c[0], -1 + c[1]],
    'R': (c) => [0 + c[0], 1 + c[1]],
}

let nextDirection = function(c, grid, currentDirection) {
    try { if ('R' != currentDirection && ('-' + letters).includes(grid.get(...nextCoordinate['L'](c)))) { return 'L' }} catch(e) {}
    try { if ('L' != currentDirection && ('-' + letters).includes(grid.get(...nextCoordinate['R'](c)))) { return 'R' }} catch(e) {}
    try { if ('U' != currentDirection && ('|' + letters).includes(grid.get(...nextCoordinate['D'](c)))) { return 'D' }} catch(e) {}
    try { if ('D' != currentDirection && ('|' + letters).includes(grid.get(...nextCoordinate['U'](c)))) { return 'U' }} catch(e) {}
}

let resolveRoute = function(coordinate, direction, grid, result) {
    var nextValue;
    var steps = 0;
    var stepIndicator = [];
    while (true) {
        try {
            coordinate = nextCoordinate[direction](coordinate);
            nextValue = grid.get(...coordinate);
            if (nextValue == undefined) { throw 'out of bounds' } 
        } catch(e) {
            return [result, stepIndicator[stepIndicator.length - 1]];
        }
        if (nextValue == '+') {
            direction = nextDirection(coordinate, grid, direction);
        }
        else if (letters.includes(nextValue)) { 
            result = result + nextValue;
            grid.replace(...coordinate, ' ');
            stepIndicator.push(steps);
        }
        if (!(letters+'|-').includes(nextValue)) { console.log(nextValue); }
        steps++;
    }
}

class Grid {
    constructor(grid) {
        this.grid = grid;
    }

    get(x, y) {
        return this.grid[x][y]
    }

    replace(x, y, replacement) {
        this.grid[x][y] = replacement;
    }
}

function partOneAndTwo(grid) {
    startCoordinate = [0, grid[0].findIndex((x) => x == '|')];
    startDirection = 'D';
    let result = resolveRoute(startCoordinate, startDirection, new Grid(grid), '');
    console.log('P1: ' + result[0]);
    console.log('P2: ' + result[1]);
};

var grid = fs.readFileSync("inp19.txt").toString().split('\n').map((x) => Array.from(x))
partOneAndTwo(grid);
