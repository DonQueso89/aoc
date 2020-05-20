"use strict";
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
var __read = (this && this.__read) || function (o, n) {
    var m = typeof Symbol === "function" && o[Symbol.iterator];
    if (!m) return o;
    var i = m.call(o), r, ar = [], e;
    try {
        while ((n === void 0 || n-- > 0) && !(r = i.next()).done) ar.push(r.value);
    }
    catch (error) { e = { error: error }; }
    finally {
        try {
            if (r && !r.done && (m = i["return"])) m.call(i);
        }
        finally { if (e) throw e.error; }
    }
    return ar;
};
var __spread = (this && this.__spread) || function () {
    for (var ar = [], i = 0; i < arguments.length; i++) ar = ar.concat(__read(arguments[i]));
    return ar;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
var e_1, _a, e_2, _b;
Object.defineProperty(exports, "__esModule", { value: true });
var fs_1 = require("fs");
var path_1 = __importDefault(require("path"));
function Guard(id_) {
    this.id_ = id_;
    this.minutes = [];
}
Guard.prototype.maxMinute = function () {
    var max = -1;
    var idx = null;
    this.minutes.map(function (e, i) {
        if (e > max) {
            max = e;
            idx = i;
        }
    });
    return [idx, max];
};
Guard.prototype.sleepTime = function () {
    return this.minutes.reduce(function (a, e) { return a + e; }, 0);
};
Guard.prototype.incr = function (minute) {
    this.minutes[minute] ? this.minutes[minute]++ : this.minutes[minute] = 1;
};
var data = fs_1.readFileSync(path_1.default.join(process.cwd(), process.argv.pop()), 'utf-8').split("\n");
data.sort(function (a, b) { return (new Date(a.slice(1, 17)) < new Date(b.slice(1, 17))) ? -1 : 1; });
var guards = {};
var guard, start, end;
try {
    for (var data_1 = __values(data), data_1_1 = data_1.next(); !data_1_1.done; data_1_1 = data_1.next()) {
        var line = data_1_1.value;
        if (line.endsWith("shift")) {
            var id_ = line.split(" ")[3].slice(1);
            guard = guards[id_] || new Guard(id_);
        }
        else if (line.endsWith("up")) {
            end = Number(line.slice(15, 17));
            try {
                for (var _c = (e_2 = void 0, __values(__spread(Array(end - start).keys()))), _d = _c.next(); !_d.done; _d = _c.next()) {
                    var x = _d.value;
                    guard.incr(start + Number(x));
                }
            }
            catch (e_2_1) { e_2 = { error: e_2_1 }; }
            finally {
                try {
                    if (_d && !_d.done && (_b = _c.return)) _b.call(_c);
                }
                finally { if (e_2) throw e_2.error; }
            }
            guards[guard.id_] = guard;
        }
        else if (line.endsWith("asleep")) {
            start = Number(line.slice(15, 17));
        }
    }
}
catch (e_1_1) { e_1 = { error: e_1_1 }; }
finally {
    try {
        if (data_1_1 && !data_1_1.done && (_a = data_1.return)) _a.call(data_1);
    }
    finally { if (e_1) throw e_1.error; }
}
var sortedBySleep = Object.values(guards);
sortedBySleep.sort(function (a, b) { return (a.sleepTime() < b.sleepTime()) ? 1 : -1; });
console.log(sortedBySleep[0].maxMinute()[0] * Number(sortedBySleep[0].id_));
sortedBySleep.sort(function (a, b) { return (a.maxMinute()[1] < b.maxMinute()[1]) ? 1 : -1; });
console.log(sortedBySleep[0].maxMinute()[0] * Number(sortedBySleep[0].id_));
