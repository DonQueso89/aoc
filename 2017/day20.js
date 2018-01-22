var fs = require("fs");

class Particle {
    constructor(p, v, a, ind) {
        this.p = p;
        this.v = v;
        this.a = a;
        this.ind = ind;
    }

    incr(ticks) {
        var c = 0
        while (c < ticks) {
            for (var i = 0; i < 3; i++) {
                this.v[i] += this.a[i];
                this.p[i] += this.v[i];
            }
            c++;
        }
        return this;
    }

    distance() {
        return this.p.reduce((s, v) => s + v, 0);
    }
}

function partOne(positions) {
    let particles = []; 
    positions = positions.replace(/\<(-?\d+,-?\d+,-?\d+)\>/g, '[$1]').split('\n');
    var p; var v; var a;
    for (var i = 0; i < positions.length; i++) {
        eval(positions[i]);
        particles.push(new Particle(p, v, a, i));
    }
    var result;
    var distances = particles.map((x) => x.incr(100).distance());
    let minDist = Math.min(...distances);
    console.log(distances.findIndex((x) => x == minDist))
};

function partTwo(particles) {
};


var positions = fs.readFileSync("inp20.txt").toString();
partOne(positions);
