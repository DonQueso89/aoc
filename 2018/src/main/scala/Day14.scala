package fun.aoc2018.day14;

object Solve extends App {
  val solvePart = args(0).toInt
  val input = args(1).toInt

  @annotation.tailrec
  def solve(nRecipes: Int, recipes: Map[Int, Int], elfOneIdx: Int, elfTwoIdx: Int): Map[Int, Int] = {
    if (recipes.size == nRecipes) {
      recipes
    } else {
      val currRecipeOne = recipes(elfOneIdx)
      val currRecipeTwo = recipes(elfTwoIdx)
      val nextSum = currRecipeOne + currRecipeTwo
      val recipesDone = recipes.size
      val recipeOne = nextSum / 10
      val recipeTwo = nextSum % 10
      if (recipeOne > 0) {
        val newRecipes = recipes ++ Map(recipesDone -> recipeOne, recipesDone +  1 -> recipeTwo)
        solve(
          nRecipes,
          newRecipes,
          (elfOneIdx + currRecipeOne + 1) % newRecipes.size,
          (elfTwoIdx + currRecipeTwo + 1) % newRecipes.size
        ) 
      } else {
        val newRecipes = recipes ++ Map(recipesDone -> recipeTwo)
        solve(
          nRecipes,
          newRecipes,
          (elfOneIdx + currRecipeOne + 1) % newRecipes.size,
          (elfTwoIdx + currRecipeTwo + 1) % newRecipes.size
        ) 
      }
    } 

  }

  @annotation.tailrec
  def solveNumLeft(number: Int, numLookBack: Int, recipes: Map[Long, Long], elfOneIdx: Long, elfTwoIdx: Long): Long = {
    println(recipes.size)
    val numberCheck = (recipes.size - numLookBack to recipes.size - 1).map(
      recipes.getOrElse(_, 0)  
    ).mkString("")

    if (numberCheck.contains(number.toString)) {
      recipes.size - numLookBack
    } else {
      val currRecipeOne = recipes(elfOneIdx)
      val currRecipeTwo = recipes(elfTwoIdx)
      val nextSum = currRecipeOne + currRecipeTwo
      val recipesDone = recipes.size.toLong
      val recipeOne = nextSum / 10
      val recipeTwo = nextSum % 10
      if (recipeOne > 0) {
        val newRecipes = recipes ++ Map[Long, Long](recipesDone -> recipeOne, recipesDone +  1L -> recipeTwo)
        solveNumLeft(
          number,
          numLookBack,
          newRecipes,
          (elfOneIdx + currRecipeOne + 1) % newRecipes.size,
          (elfTwoIdx + currRecipeTwo + 1) % newRecipes.size
        ) 
      } else {
        val newRecipes = recipes ++ Map[Long, Long](recipesDone -> recipeTwo)
        solveNumLeft(
          number,
          numLookBack,
          newRecipes,
          (elfOneIdx + currRecipeOne + 1) % newRecipes.size,
          (elfTwoIdx + currRecipeTwo + 1) % newRecipes.size
        ) 
      }
    } 

  }

  if (solvePart == 1) {
    val result = solve(input + 10, Map(0 -> 3, 1 -> 7), 0, 1).filterKeys(
      _ >= input
    ).toList.sortBy(
      _._1
    ).map(
      _._2
    )
    println(s"Part 1: ${result.mkString("")}")
  } else {
    val result = solveNumLeft(input, input.toString.size, Map(0L -> 3L, 1L -> 7L), 0L, 1L)
    println(s"Part 2: $result")
  }
}
