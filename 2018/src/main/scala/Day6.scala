package fun.aoc2018.day6
import scala.io.Source

object Solve extends App {
  if (args.length < 2) {
    println("input path and dist limit required")
  }

  implicit class ManhattanDistance(t: (Int, Int)) {
    def ***(p: (Int, Int)) = (p._1 - t._1).abs + (p._2 - t._2).abs
  }

  def coordinateStream(head: (Int, Int), maxY: Int, maxX: Int): Stream[(Int, Int)] = {
    if (head._2 > maxX) {
      Stream.empty
    } else if (head._1 == maxY) {
      Stream.cons(head, coordinateStream((0, head._2 + 1), maxY, maxX))
    } else {
      Stream.cons(head, coordinateStream((head._1 + 1, head._2), maxY, maxX))
    }
  }

  @annotation.tailrec
  def resolve(coordinateState: Map[(Int, Int), Int], gridWalker: Stream[(Int, Int)], sumNearest: Int, limit: Int): (Int, Int) = {
    if (gridWalker.isEmpty) {
      return((coordinateState.filter(t => t._2 > -1).values.max, sumNearest))
    }
    
    val location = gridWalker.head
    val distances = coordinateState.keys.toList.map((e) => (e, location *** e))
    val minimumDistance = distances.map(_._2).min
    val closest = distances.filter(_._2 == minimumDistance).map(_._1)
    val isNearEnough = distances.map(_._2).sum < limit
    
    if (closest.size == 1) {
      val value  = coordinateState.get(closest.head).get
      val isInfinite = value == -1 || location._1 == 0 || location._2 == 0 || location._1 == maximumY || location._2 == maximumX
      resolve(
        coordinateState ++ Map(closest.head -> { if (isInfinite) -1 else value + 1 } ),
        gridWalker.tail,
        if (isNearEnough) sumNearest + 1 else sumNearest,
        limit
      )
    } else {
      resolve(
        coordinateState,
        gridWalker.tail,
        if (isNearEnough) sumNearest + 1 else sumNearest,
        limit
      )
    }
  }
  
  lazy val coordinates: Map[(Int, Int), Int] = Source.fromFile(
    args(0)
  ).getLines.map(
    s => s.split(',').map(_.trim.toInt)
  ).map(
    t => ((t(0), t(1)), 0) 
  ).toMap
  
  lazy val maximumY = coordinates.keys.map(_._1).max
  lazy val maximumX = coordinates.keys.map(_._2).max

  val answers = resolve(
    coordinates,
    coordinateStream((0, 0),
      maximumY,
      maximumX
    ),
    0,
    args(1).toInt
  )
  println(s"Part 1: ${answers._1}")
  println(s"Part 2: ${answers._2}")
}
