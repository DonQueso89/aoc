package fun.aoc2018.day11;

object Solve extends App {
  val gridSerialNumber = args(0).toLong

  def cellStream(
    head: (Long, Long),
    minX: Long,
    minY: Long,
    maxX: Long,
    maxY: Long
  ): Stream[(Long, Long)] = {
    if (head._2 > maxY) {
      Stream.empty
    } else if (head._1 == maxX) {
      Stream.cons(head, cellStream((minX, head._2 + 1), minX, minY, maxX, maxY))
    } else {
      Stream.cons(head, cellStream((head._1 + 1, head._2), minX, minY, maxX, maxY))
    }
  }
  
  val powerLevel: ((Long, Long)) => Long = { 
    case (x, y) =>  ((x + 10) * y + gridSerialNumber) * (x  + 10) / 100 % 10 - 5 
  }

  @annotation.tailrec
  def constructGrid(grid: Map[(Long, Long), Long], cells: Stream[(Long, Long)]): Map[(Long, Long), Long] = {
    // x, y -> powerlevel
    cells.headOption match {
      case Some(cell) => constructGrid(
        grid ++ Map((cell._1, cell._2) -> powerLevel(cell)),
        cells.tail
      );
      case None => grid;
    }
  }
  
  @annotation.tailrec
  def resolveMax(
    gridWalker: Stream[(Long, Long)],
    grid: Map[(Long, Long), Long],
    result: (Long, Long, Long),
    northWestOffset: Int,
    southEastOffset: Int
  ): (Long, Long, Long) = {
    gridWalker.headOption match {
      case Some(cell) => {
        val (x, y) = cell
        val subGrid: Stream[(Long, Long)] = cellStream(
          (x - northWestOffset, y - northWestOffset),
          x - northWestOffset,
          y - northWestOffset,
          x + southEastOffset,
          y + southEastOffset
        )
        val gridPower = subGrid.foldLeft(0L)(
          (acc: Long, subCell: (Long, Long)) => grid(subCell) + acc
        )
        if (gridPower > result._3) {
          resolveMax(
            gridWalker.tail,
            grid,
            (x - northWestOffset, y - northWestOffset, gridPower),
            northWestOffset,
            southEastOffset
          )
        } else {
          resolveMax(
            gridWalker.tail,
            grid,
            result,
            northWestOffset,
            southEastOffset
          )
        }
      };
      case None => result
    }
  }

  lazy val powerGrid = constructGrid(Map[(Long, Long), Long](), cellStream((1, 1), 1, 1, 300, 300))
  lazy val maxPower = resolveMax(
    cellStream((2, 2), 2, 2, 299, 299),
    powerGrid,
    (0L, 0L, 1L << 63), // x, y, power
    1,
    1
  )
  println(s"Part 1: X: ${maxPower._1} Y: ${maxPower._2} Power: ${maxPower._3}")
  val maxPerSize = (10 to 16).toList.map(size => {
    val topLeftOffset = if (size % 2 == 0) size / 2 - 1 else size / 2
    val bottomRightOffset = size / 2
    val start = topLeftOffset + 1
    val maxForSize = resolveMax(
      cellStream(
        (start, start),
        start,
        start,
        300 - bottomRightOffset,
        300 - bottomRightOffset
      ),
      powerGrid,
      (0L, 0L, 1L << 63), // x, y, power
      topLeftOffset,
      bottomRightOffset
    )
    (maxForSize._1, maxForSize._2, maxForSize._3, size)
  })
  val maxAcrossSizes = maxPerSize.sortWith(_._3 > _._3)(0)
  println(s"Part 2: X: ${maxAcrossSizes._1} Y: ${maxAcrossSizes._2} size: ${maxAcrossSizes._4}")
}
