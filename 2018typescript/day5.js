"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
exports.__esModule = true;
var fs_1 = require("fs");
var path_1 = __importDefault(require("path"));
var inputPath = path_1["default"].join(process.cwd(), 'input5');
var data = Array.from(fs_1.readFileSync(inputPath, 'utf-8'));
console.log(data);
var pointer = 0;
while (pointer < data.length - 1) {
    var a = data[pointer];
    if (data.length > 1) {
        if (Math.abs(a.charCodeAt(0) - data[pointer + 1].charCodeAt(0)) == 32) {
            data.splice(pointer, 2);
            pointer = Math.max(pointer - 1, 0);
        }
        else if (pointer > 0 && Math.abs(a.charCodeAt(0) - data[pointer - 1].charCodeAt(0)) == 32) {
            data.splice(pointer - 1, 2);
            pointer = Math.max(pointer - 2, 0);
        }
        else {
            pointer++;
        }
    }
}
console.log(data.length);
