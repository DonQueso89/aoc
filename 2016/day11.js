var __values = (this && this.__values) || function(o) {
    var s = typeof Symbol === "function" && Symbol.iterator, m = s && o[s], i = 0;
    if (m) return m.call(o);
    if (o && typeof o.length === "number") return {
        next: function () {
            if (o && i >= o.length) o = void 0;
            return { value: o && o[i++], done: !o };
        }
    };
    throw new TypeError(s ? "Object is not iterable." : "Symbol.iterator is not defined.");
};
function Floor(floorState) {
    this.state = floorState || [];
}
Floor.prototype.toString = function () {
    return this.state.map(function (x) { return " " + x + " "; }).join(' | ');
};
function Elevator(a, b) {
    this.a = a;
    this.b = b;
}
Elevator.prototype.toString = function () {
    return "E| " + (this.a || "  ") + " | " + (this.b || "  ") + " ";
};
function State(f1, f2, f3, f4) {
    this.f1 = f1 || new Floor();
    this.f2 = f2 || new Floor();
    this.f3 = f3 || new Floor();
    this.f4 = f4 || new Floor();
}
State.prototype.toString = function () {
    var _this = this;
    return [1, 2, 3, 4].map(function (i) { return ("F" + i + "| " + _this['f' + i] + " |").padEnd(20); }).join('\n');
};
var chips = ['THC', 'PLC', 'STC', 'PRC', 'RUC'];
function isValid(floor) {
    var e_1, _a;
    if (floor.state.length > 1) {
        try {
            for (var chips_1 = __values(chips), chips_1_1 = chips_1.next(); !chips_1_1.done; chips_1_1 = chips_1.next()) {
                var e = chips_1_1.value;
                if (!floor.state.includes(e)) {
                    continue;
                }
                if (floor.state.includes((e.slice(0, 2) + 'G'))) {
                    continue;
                }
                else if (floor.state.find(function (x) { return x.endsWith('G'); })) {
                    return false;
                }
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (chips_1_1 && !chips_1_1.done && (_a = chips_1.return)) _a.call(chips_1);
            }
            finally { if (e_1) throw e_1.error; }
        }
    }
    return true;
}
function FloorCycle(current) {
    if (current) {
        this.idx = Number(this.current.slice(1) - 1);
    }
    else {
        this.idx = 0;
    }
}
FloorCycle.prototype.next = function () {
    this.idx = (this.idx + 1) % 4;
    return 'f' + (this.idx + 1);
};
FloorCycle.prototype.last = function () {
    this.idx = this.idx - 1;
    if (this.idx < 0) {
        this.idx = 3;
    }
    return 'f' + (this.idx + 1);
};
function next(state, floorCycle, elevator, steps) {
    if (steps === void 0) { steps = 0; }
    if (state.f4.state.length == 10) {
        console.log("Done in " + steps + " steps");
        return steps;
    }
}
var state = new State(new Floor(['THG', 'THC', 'PLG', 'STG']), new Floor(['PLC', 'STC']), new Floor(['PRG', 'PRC', 'RUG', 'RUC']));
var elevator = new Elevator();
var floorCycle = new FloorCycle();
