import { readFileSync } from 'fs'
import path from 'path'

let inputPath = path.join(process.cwd(), 'input5')
let data = Array.from(readFileSync(inputPath, 'utf-8'))

let pointer = 0
while (pointer < data.length - 1) {
  let a = data[pointer]
  if (data.length > 1) {
    if (Math.abs(a.charCodeAt(0) - data[pointer + 1].charCodeAt(0)) == 32) {
      data.splice(pointer, 2)
      pointer = Math.max(pointer - 1, 0)
    } else if (pointer > 0 && Math.abs(a.charCodeAt(0) - data[pointer - 1].charCodeAt(0)) == 32) {
      data.splice(pointer - 1, 2)
      pointer = Math.max(pointer - 2, 0)
    } else {
      pointer++
    }
  }
}

console.log(data.length)
