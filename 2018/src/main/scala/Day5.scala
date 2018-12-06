package fun.aoc2018.day5

import scala.concurrent._
import ExecutionContext.Implicits.global
import scala.math
import scala.io.Source

object Solve extends App {
  lazy val input: String = Source.fromFile("input5").getLines.mkString

  val triggersReaction = (x:Char, y:Char) => (x -  y).abs == 32

  @annotation.tailrec
  def chainReact(polymer: String, index: Int): String = {
    if (index + 1 == polymer.size) {
      polymer
    }
    else if (triggersReaction(polymer(index), polymer(index + 1))) {
      chainReact(
        polymer.slice(0, index) ++ polymer.slice(index + 2, polymer.size),
        math.max(index - 1, 0)
      )
    } else {
      chainReact(polymer, index + 1)
    }
  }

  println("Part 1: " + chainReact(input, 0).size.toString)
  
  val workers: Seq[Future[Int]] = ('a' to 'z').map((x: Char) => { Future { chainReact(input.replaceAll(x.toString, "").replaceAll(x.toString.toUpperCase, ""), 0).size } })

  while (workers.exists((f: Future[Int]) => !f.isCompleted)) {
    Thread.sleep(1000)
    println("Working...")
  }

  println("Part 2: " + workers.map(_.value.get.get).min)
}
