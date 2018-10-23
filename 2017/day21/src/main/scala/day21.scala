package day.twentyOne

import scala.io.Source

class Solution {
  /*
   *A   B   C   D
    010 100 111 011
    001 101 100 101
    111 110 010 001

    010/001/111
    111/001/010 A and A reversed

    100/101/110 B = [[x[0] for x in A], [x[1] for x in A], x[2] for x in A]]
    110/101/100

    010/100/111
    111/100/010 C = A with elems reversed

    001/101/011 B with elems reversed
    011/101/001
   * inp = 108 lines so we need max 108 * 8 rules
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
    val rules = Source
      .fromFile("inp21.txt")
      .getLines
      .map({ 
        case(m) => val v = m.replaceAll(" ", "").split("=>"); (v(0).split("/").toList, v(1).split("/").toList) 
      })
      .toMap

    rules
    .foldLeft(rules)({
      case(result, (permutation, output)) => {
        result ++ getPermutations(permutation).map((_, output)).toMap
      }
    })
  }

  def resolve(pixel: List[String], maxDepth: Int, rules: Map[List[String], List[String]]): Int = {
    println(pixel, maxDepth)
    if (maxDepth == 0) {
      pixel.mkString.count(_ == '#')
    } else {
      val enhancedPixel = rules.get(pixel).get.mkString
      if (enhancedPixel.size % 2 ==  0) {
        enhancedPixel
          .grouped(4)
          .toList
          .map(_.grouped(2).toList)
          .map(pix => resolve(pix, maxDepth - 1, rules))
          .reduce(_ + _)
      } else {
        enhancedPixel
          .grouped(9)
          .toList
          .map(_.grouped(3).toList)
          .map(pix => resolve(pix, maxDepth - 1, rules))
          .reduce(_ + _)
      }
    }
  }
}

object Run extends App {
}
