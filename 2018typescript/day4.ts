import { readFileSync } from 'fs'
import path from 'path'

interface Guard {
  id_: string
  minutes: Object
  maxMinute: () => [number, number]
  sleepTime: () => number
  incr: (number) => void
}

function Guard(id_) {
  this.id_ = id_
  this.minutes = []
}

Guard.prototype.maxMinute = function() {
  var max = -1
  var idx = null
  this.minutes.map((e, i) => {
    if (e > max) {
      max = e
      idx = i
    }
  })
  return [idx, max]
}
Guard.prototype.sleepTime = function() {
  return this.minutes.reduce((a, e) => a + e, 0)
}

Guard.prototype.incr = function(minute: number) {
  this.minutes[minute] ? this.minutes[minute]++ : this.minutes[minute] = 1
}


let data: Array<string> = readFileSync(path.join(process.cwd(), process.argv.pop()), 'utf-8').split("\n")
data.sort(
  (a, b) => (new Date(a.slice(1, 17)) < new Date(b.slice(1, 17))) ? -1 : 1
)

let guards = {}
var guard, start, end;


for (let line of data) {
  if (line.endsWith("shift")) {
    let id_ = line.split(" ")[3].slice(1)
    guard = guards[id_] || new Guard(id_)
  } else if (line.endsWith("up")) {
    end = Number(line.slice(15, 17))
    for (let x of [...Array(end - start).keys()]) { 
      guard.incr(start + Number(x))
    }
    guards[guard.id_] = guard
  } else if (line.endsWith("asleep")) {
    start = Number(line.slice(15, 17))
  }
}


let sortedBySleep: Array<Guard> = Object.values(guards)
sortedBySleep.sort((a: Guard, b: Guard) => (a.sleepTime() < b.sleepTime()) ? 1 : -1)

console.log(sortedBySleep[0].maxMinute()[0] * Number(sortedBySleep[0].id_))


sortedBySleep.sort((a: Guard, b: Guard) => (a.maxMinute()[1] < b.maxMinute()[1]) ? 1 : -1)
console.log(sortedBySleep[0].maxMinute()[0] * Number(sortedBySleep[0].id_))
