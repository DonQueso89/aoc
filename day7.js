let fs = require("fs");

let getRoot = function(d) {
    var nonLeafNodes = d.filter((x) => x.split(' ').length > 2);
    var nonRootNodes = nonLeafNodes.reduce(function(s, v) {
        v = v.replace(/,/g, '').split(' ');
        s.push(...v.slice(3, v.length));
        return s;
    }, []);
    nonLeafNodes = nonLeafNodes.map((x) => x.split(' ')[0]);
    var difference = new Set([...nonLeafNodes].filter(x => !new Set(nonRootNodes).has(x)));
    return difference;
}

var resolveWeight = function(currentNode, nodeMapping, weightMapping) {
    var children = nodeMapping[currentNode];
    if (children == undefined) {
        return weightMapping[currentNode];
    } else {
        result = children.map((child) => resolveWeight(child, nodeMapping, weightMapping));

        var b = true;
        for (var i = 0; i < result.length; i++) {
            b &= (result[i] == result[(i + 1) % result.length]);
        }
        if (!b) {
            console.log('Sum: ' + result);
            console.log('Weigths of children: ' + children.map((x) => weightMapping[x]));
        }

        return weightMapping[currentNode] + result.reduce((s, v) => s+v);
    }   

}


let partTwo = function(d) {
    var weightMapping = new Object();
    var nodeMapping = new Object();
    let root = Array.from(getRoot(d))[0];

    for (var i = 0; i < d.length; i++) {
        var line = d[i].split(' ');
        var key = line[0];
        var weight = Number(line[1].replace(/[()]/g, ''));
        weightMapping[key] = weight;
    }
    var nonLeafNodes = d.map((x) => x.split(' ')).filter((x) => x.length > 2);

    for (var i = 0; i < nonLeafNodes.length; i++) {
        nonLeafNodes[i] = nonLeafNodes[i].map((x) => x.replace(/,/g, ''));
        nodeMapping[nonLeafNodes[i][0]] = nonLeafNodes[i].slice(3, nonLeafNodes[i].length);
    }

    var children = nodeMapping[root];

    for (var i = 0; i < children.length; i++) {
        resolveWeight(children[i], nodeMapping, weightMapping);
    }

}

var data = [];
//data.push(fs.readFileSync("testinp7.txt").toString().split("\n"));
data.push(fs.readFileSync("inp7.txt").toString().split("\n"));
data.map(partTwo);
