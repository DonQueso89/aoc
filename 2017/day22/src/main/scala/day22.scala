package day.twentyTwo
import scala.io.Source


class Solution(inputPath: String) {
  val numEncode = (c: Char) => if (c == '#') 1 else 0
  val gridState: Map[(Int, Int), Int] = Source
    .fromFile(inputPath)
    .getLines
    .toList
    .zipWithIndex
    .map({ case (r, ri) => r.zipWithIndex.map({case (c, ci) => Map((ri, ci) -> numEncode(c))})})
    .flatten
    .foldLeft(Map[(Int, Int), Int]())({case(r,e) => r ++ e})

  val nextPosition = List(
    (x: Int, y: Int) => (x - 1, y), // N
    (x: Int, y: Int) => (x, y + 1), // E
    (x: Int, y: Int) => (x + 1, y), // S
    (x: Int, y: Int) => (x, y - 1)  // W
  )

  val middle: Int = Math.sqrt(gridState.size) / 2 toInt
  val beginPosition = (middle, middle)
  val direction = 0
  val numDirections = 4

  @annotation.tailrec
  final def solve(curGrid: Map[(Int, Int), Int], numBursts: Int, curDir: Int, curPos: (Int, Int), numInfects: Int): Int = {
    if (numBursts == 0) {
      numInfects

    } else {
      val curNode = curGrid.getOrElse(curPos, 0)
      val isInfected = curNode == 1
      val nextDir = (if (isInfected) curDir + 1 else curDir - 1) % numDirections

      solve(
        curGrid ++ Map(curPos -> (if (isInfected) 0 else 1)),
        numBursts - 1,
        nextDir,
        nextPosition(if (nextDir < 0) numDirections + nextDir else nextDir)(curPos._1, curPos._2),
        if (isInfected) numInfects else numInfects + 1
      )
    }
  }

  @annotation.tailrec
  final def solveEvolved(curGrid: Map[(Int, Int), Int], numBursts: Int, curDir: Int, curPos: (Int, Int), numInfects: Int): Int = {
    /*
     * part 1 with more states and more turns
     */
    if (numBursts == 0) {
      numInfects
    } else {
      val nodeState = curGrid.getOrElse(curPos, 0)

      val nextNodeState = nodeState match {
        case 0 => 2 // clean -> weakened
        case 1 => 3 // infected -> flagged 
        case 2 => 1 // weakened -> infected
        case 3 => 0 // flagged -> clean
      }
       
      val nextDir = (nodeState match {
        case 0 => curDir - 1 // clean = 90 left
        case 1 => curDir + 1 // infected = 90 right
        case 3 => curDir + 2 // flagged = 180
        case _ => curDir // weakened = no turn
      }) % numDirections

      solveEvolved(
        curGrid ++ Map(curPos -> nextNodeState),
        numBursts - 1,
        nextDir,
        nextPosition(if (nextDir < 0) numDirections + nextDir else nextDir)(curPos._1, curPos._2),
        if (nodeState == 2) numInfects + 1 else numInfects
      )
    }
  }
}

object Run extends App {
  val s = new Solution("inp22.txt")
  println("Part 1: " + s.solve(s.gridState, 10000, 0, s.beginPosition, 0))
  println("Part 2: " + s.solveEvolved(s.gridState, 10000000, 0, s.beginPosition, 0))
}
