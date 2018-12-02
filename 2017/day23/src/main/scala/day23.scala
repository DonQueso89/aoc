package day.twentyThree
import scala.io.Source
import scala.util.Try


class Solution {
  val funcs = Map[String, (Int, Int) => Int](
    "set" -> {(r: Int, v: Int) => v},
    "sub" -> {(r: Int, v: Int) => r - v},
    "mul" -> {(r: Int, v: Int) => r * v},
  )

  val jump = (p: Int, c: Int, v: Int) => if (c != 0) p + v else p + 1
  val isNonNumeric = (s: String) => raw"^[a-z]{1}$$".r.findFirstIn(s).nonEmpty

  val instructions = Source
    .fromFile("inp23.txt")
    .getLines
    .toList
    .map(_.split(" "))
    .toList

  def fastForward(stateBeforeLoop: Map[Char, Int], stateAfterLoop: Map[Char, Int], jumpCondition: Char, pointer: Int, priorPointer: Int): (Int, Map[Char, Int]) = {
    println(stateBeforeLoop)
    println(stateAfterLoop)
    val jumpConditionValue = stateAfterLoop(jumpCondition)
    val jumpConditionDelta = jumpConditionValue - stateBeforeLoop.getOrElse(jumpCondition, 0)
    val numLoopsToZero = jumpConditionValue.abs / jumpConditionDelta.abs // assuming we're going to hit 0 at some point
    val numMults = numLoopsToZero * instructions.slice(priorPointer, pointer).filter(_(0) == "mul").size

    (numMults * numLoopsToZero, stateAfterLoop.map({ case(k, v) => (k, v + (v - stateBeforeLoop(k)) * numLoopsToZero) }))
  }

  @annotation.tailrec
  final def solve(state: Map[Char, Int], result: Int, pointer: Int = 0, loopState: Map[Int, Map[Char, Int]]): Int = {
    if (pointer < 0 || pointer >= instructions.size) {
      result
    } else {
      val func: String = instructions(pointer)(0)
      val arg1: String = instructions(pointer)(1)
      val arg2: String = instructions(pointer)(2)

      val parsedArg1: Int = Try(arg1.toInt).getOrElse(state.getOrElse(arg1(0), 0))
      val parsedArg2: Int = Try(arg2.toInt).getOrElse(state.getOrElse(arg2(0), 0))

      if (func == "jnz") {
        val jumpSignature = s"$func($pointer, $arg1, $arg2)"
        if (parsedArg2 == -13 || parsedArg2 == -23) {
          println(jumpSignature)
          println(state)
        }
        if (loopState.get(jumpSignature).nonEmpty) {
          // We are in a loop, fast forward to the end
          val (resultDuringLoop, stateAfterLoop) = fastForward(loopState.get(jumpSignature).get, state, arg1(0), pointer, pointer - parsedArg2)
          solve(
            stateAfterLoop,
            result + resultDuringLoop,
            pointer + 1,
            loopState.filter(_ != jumpSignature) // refresh loopState
          )
        } else if(isNonNumeric(arg1) && parsedArg1 != 0 && parsedArg2 < 0) {
          // Save the jump signature with its state if the jump condition is variable and non-zero and we're jumping back
          solve(state, result, jump(pointer, parsedArg1, parsedArg2), loopState ++ Map(s"$func($pointer, $arg1, $arg2)" -> state))
        } else {
          // Just keep going
          solve(state, result, jump(pointer, parsedArg1, parsedArg2), loopState)
        }
      } else {
        solve(
          state ++ Map(arg1(0) -> funcs(func)(parsedArg1, parsedArg2)),
          if (func == "mul") result + 1 else result,
          pointer + 1,
          loopState
        )
      }
    }
    
  }
}

object Run extends App {
  val s = new Solution()
  println("Part 1: " + s.solve(Map[Char, Int](), 0, 0, Map[Int, Map[Char, Int]]()))
  println("Part 2: " + s.solve(Map[Char, Int]('a' -> 1), 0, 0, Map[Int, Map[Char, Int]]()))
}
