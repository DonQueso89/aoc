var fs = require("fs");

let countNodes = function(currentNode, nodeMapping, nodesVisited) {
    // Get children from nodeMapping, removing visited nodes
    nodesVisited.push(currentNode);
    var children = nodeMapping[currentNode].filter((x) => !nodesVisited.includes(x));
    nodesVisited.push(...children);
    if (children.length == 0) {
        return 1 // This is a leaf node
    }
    // Get the count for each child
    var sum = 0;
    for (var i = 0; i < children.length; i++) {
        var child = children[i];
        sum += countNodes(child, nodeMapping, nodesVisited);
    }
    return 1 + sum;
}

let traverseGroup = function(currentNode, nodeMapping, nodesVisited) {
    // Get children from nodeMapping, removing visited nodes
    nodesVisited.add(currentNode);
    var children = nodeMapping[currentNode].filter((x) => !nodesVisited.has(x));
    nodesVisited.add(...children);
    if (children.length == 0) {
        return // This is a leaf node
    }
    for (var i = 0; i < children.length; i++) {
        var child = children[i];
        traverseGroup(child, nodeMapping, nodesVisited);
    }
    return
}

let partOne = function(pipes) {
    var nodeMapping = new Object();
    for (var i = 0; i < pipes.length; i++) {
        var pipe = pipes[i];
        nodeMapping[pipe[0]] = pipe.slice(1, )
    }
    let result = countNodes(0, nodeMapping, []);
    console.log('P1: ' + result);
}

let partTwo = function(pipes){
    var nodeMapping = new Object();
    for (var i = 0; i < pipes.length; i++) {
        var pipe = pipes[i];
        nodeMapping[pipe[0]] = pipe.slice(1, )
    }
    var nodesVisited = new Set();
    var nGroups = 0;
    var currentRoot = 0;
    var nodesUnvisited = Object.keys(nodeMapping).map(Number);
    while (nodesUnvisited.length > 0) {
        traverseGroup(currentRoot, nodeMapping, nodesVisited);
        nGroups += 1;
        nodesUnvisited = nodesUnvisited.filter((x) => !nodesVisited.has(x));
        currentRoot = nodesUnvisited[0];
    }
    console.log('P2: ' + nGroups);
}


var pipes = fs.readFileSync("inp12.txt").toString().replace(/<->/g, '').replace(/,/g, '').split('\n').map(function(x) {
    x = x.split(' '); 
    x.splice(1, 1);
    x = x.map(Number);
    return x;
});

//partOne(pipes);
partTwo(pipes);
