package day.twentyOne

import scala.io.Source
import scala.collection.mutable.ListBuffer

class Solution {
  /*
   * #../.../... => ####/####/.###/####
   */
  val initialValue = List[String](".#.","..#","###")

  def getPermutations(permutation: List[String]): List[List[String]] = {
    /*
     * if the given perm = A
     * A rotated 180 degrees is A with its elems reversed
     * and the rest can be derived from rotating A by 90 degrees
     */
    val rotated90: List[String] = (0 until permutation.size)
      .toList
      .map(i => permutation.map(_(i).toString).mkString)

    List(
      permutation.reverse,
      permutation.map(_.reverse),
      permutation.map(_.reverse).reverse,
      rotated90,
      rotated90.reverse,
      rotated90.map(_.reverse),
      rotated90.map(_.reverse).reverse
    )
  }
  
  /*
    * Rules with possible permutations pointing to the same output
    */
  def getRules: Map[List[String], List[String]] = { 
    val initialRules = Source
      .fromFile("inp21.txt")
      .getLines
      .map({ 
        case(m) => val v = m.replaceAll(" ", "").split("=>"); (v(0).split("/").toList, v(1).split("/").toList) 
      })
      .toMap
    
    initialRules
      .foldLeft(initialRules)({
        case(result, (permutation, output)) => {
          result ++ getPermutations(permutation).map((_, output)).toMap
        }
    })
  }

  def assemble(pixels: List[List[String]]): List[String] = {
    /*
     * Assemble pixels into a new square
     */
    val numRows = Math.sqrt(pixels.size).toInt
    pixels
      .grouped(numRows)
      .toList
      .map(subList => subList.transpose)
      .flatten
      .flatten
  }


  def splitTwoByTwo(pixel: List[String]):List[List[String]] = {
    val size = Math.sqrt(pixel.flatten.size).toInt
    val numCols = size / 2
    val grouped = pixel
      .mkString
      .grouped(2)
      .toList
    
    // Re-order the groups to get the pixels in order
    var newPixels = ListBuffer[List[String]]()

    for (row <- 0 until grouped.size by size) {
      for (col <- row until row + numCols) {
        newPixels += List(grouped(col), grouped(col + numCols))
      }
    }
    newPixels.toList
  }

  def splitThreeByThree(pixel: List[String]):List[List[String]] = {
    val size = Math.sqrt(pixel.flatten.size).toInt
    val numCols = size / 3
    val grouped = pixel
      .mkString
      .grouped(3)
      .toList

    var newPixels = ListBuffer[List[String]]()

    // Re-order the groups to get the pixels in order
    for (row <- 0 until grouped.size by size) {
      for (col <- row until row + numCols) {
        newPixels += List(grouped(col), grouped(col + numCols), grouped(col + numCols * 2))
      }
    }
    newPixels.toList
  }

  def solve(initialPixel: List[String], maxDepth: Int): Int = {
    val rules = getRules
    var currentPixel = initialPixel
    for (i <- 0 until maxDepth) {
        val pixelSize = Math.sqrt(currentPixel.mkString.size).toInt
        if (pixelSize % 2 ==  0) {
          currentPixel = assemble(splitTwoByTwo(currentPixel).map(rules.get(_).get))
        } else {
          currentPixel = assemble(splitThreeByThree(currentPixel).map(rules.get(_).get))
        }
    }
    currentPixel.mkString.count(_ == '#')
  }
}

object Run extends App {
}
