type RTG = 'THG' | 'PLG' | 'STG' | 'PRG' | 'RUG' | undefined
type Chip = 'THC' | 'PLC' | 'STC' | 'PRC' | 'RUC' | undefined
type Hardware = RTG | Chip

interface Elevator {
  a: Hardware
  b: Hardware
}

interface Floor {
  state: Array<Hardware>
}

function Floor(floorState?: Array<Hardware>) {
  this.state = floorState || []
}

Floor.prototype.toString = function() {
  return this.state.map(x => ` ${x} `).join(' | ')
}

interface State {
  f1: Floor
  f2: Floor
  f3: Floor
  f4: Floor
}


function Elevator(a?: Hardware, b?: Hardware) {
  this.a = a
  this.b = b
}

Elevator.prototype.toString = function() {
  return `E| ${this.a || "  "} | ${this.b || "  "} `
}

function State(f1?, f2?, f3?, f4?) {
  this.f1 = f1 || new Floor()
  this.f2 = f2 || new Floor()
  this.f3 = f3 || new Floor()
  this.f4 = f4 || new Floor()
}

State.prototype.toString = function() {
  return [1, 2, 3, 4].map(i => `F${i}| ${this['f' + i]} |`.padEnd(20)).join('\n')
}

const chips: Array<Hardware> = ['THC', 'PLC', 'STC', 'PRC', 'RUC']

function isValid(floor: Floor): boolean {
  if (floor.state.length > 1) {
    for (let e of chips) {
      if (!floor.state.includes(e)) {
        continue
      }
      if (floor.state.find(x => x == e.slice(0, 2) + 'G')) {
        continue 
      }
      else if (floor.state.find(x => x.endsWith('G'))) {
        return false
      }
    }
  }
  return true
}


/*
 * The first floor contains a thulium generator, a thulium-compatible microchip, a plutonium generator, and a strontium generator.
The second floor contains a plutonium-compatible microchip and a strontium-compatible microchip.
The third floor contains a promethium generator, a promethium-compatible microchip, a ruthenium generator, and a ruthenium-compatible microchip.
The fourth floor contains nothing relevant.
 */

type FloorKey = 'f1' | 'f2' | 'f3' | 'f4' | undefined

interface FloorCycle {
  idx: number
  next: () => string
  last: () => string
}

function FloorCycle(current?: FloorKey) {
  if (current) {
    this.idx = Number(this.current.slice(1) - 1)
  } else {
    this.idx = 0
  }
}

FloorCycle.prototype.next = function() {
  this.idx = (this.idx + 1) % 4
  return 'f' + (this.idx + 1)
}

FloorCycle.prototype.last = function() {
  this.idx = this.idx - 1
  if (this.idx < 0) {
    this.idx = 3
  }
  return 'f' + (this.idx + 1)
}

function next(state: State, floorCycle: FloorCycle, elevator: Elevator, steps: number = 0) {
  if (state.f4.state.length == 10) {
    console.log(`Done in ${steps} steps`)
    return steps
  }
}

let state = new State(
  new Floor(['THG', 'THC', 'PLG', 'STG']),
  new Floor(['PLC', 'STC']),
  new Floor(['PRG', 'PRC', 'RUG', 'RUC'])
)

let elevator = new Elevator()
let floorCycle= new FloorCycle()
