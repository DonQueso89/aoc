package day.twenty

import scala.io.Source

// position, velocity, acceleration
case class Axis(p: Int, v: Int, a: Int)
case class Particle(px: Int, py: Int, pz: Int, vx: Int, vy: Int, vz: Int, ax: Int, ay: Int, az: Int) {
  val x = Axis(px, vx, ax)
  val y = Axis(py, vy, ay)
  val z = Axis(pz, vz, az)

  val manhattanAcceleration = x.a.abs + y.a.abs + z.a.abs
  val position = (x.p, y.p, z.p)
  
  def nextState: Particle = {
    Particle(
      px + vx + ax,
      py + vy + ay,
      pz + vz + az,
      vx + ax,
      vy + ay,
      vz + az,
      ax,
      ay,
      az
    )
  }
}
class Solution {
  def getParticles(): List[Particle] = {
    /*
    * Get input from the file as Particles
    */
    val inp = Source.fromFile("inp20.txt").getLines.toList
    def filterChars(c: Character): Boolean = !List('<', '>', '=', 'p', 'v', 'a').contains(c)
    inp.map((line) => {
      val props: List[Int] = line
        .replaceAll(" ", "")    // remove whitespace
        .filter(filterChars(_)) // filter out thrash
        .split(",")             // to Array[String]
        .toList                 // to List[String]
        .map(_.toInt)           // to List[Int]

      props match {
        case List(px, py, pz, vx, vy, vz, ax, ay, az) => Particle(px, py, pz, vx, vy, vz, ax, ay, az)
      }
    }) 
  }

  // Calc dist after 50, 100 and 200 ticks
  val particles: List[Particle] = getParticles()

}

object Run extends App {
  def filterCollided(p: List[Particle]): List[Particle] = {
    /*
     * Group by position, filter duplicates
     */
    p.foldLeft(Map[(Int, Int, Int), List[Particle]]())(
      (result, particle) => {
        val value = particle :: result.getOrElse(particle.position, List[Particle]())
        result.updated(particle.position, value)
      }
    )
    .filterNot({ case (k, v) => v.size > 1 })
    .values
    .flatten
    .toList
  }

  @annotation.tailrec
  def resolveCollisions(p: List[Particle], waitSinceLastCollision: Int, init: Int): List[Particle] = {
    if (waitSinceLastCollision == 0) {
      p
    } else {
      val filtered = filterCollided(p.map(_.nextState))
      resolveCollisions(filtered, if (filtered.size < p.size) init else waitSinceLastCollision - 1, init)
    }
  }

  // Acceleration is the only thing that counts in the long run
  val particles = new Solution().particles
  println(s"Min manhattan acceleration ${particles.zipWithIndex.minBy(_._1.manhattanAcceleration)._2}")
  println(s"Particles left after collision resolution ${resolveCollisions(particles, 100000, 100000).size}")
}
