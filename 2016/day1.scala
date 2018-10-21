import scala.io.Source
import util.control.Breaks._

object Main {
  def readInp(): String = {
      return(Source.fromFile("inp1.txt").getLines.mkString)
  }

  def up(x: Integer, y: Integer, n: Integer): (Integer, Integer) = {
    return (x, y + n);
  }
  
  def down(x: Integer, y: Integer, n:Integer): (Integer, Integer) = {
    return (x, y - n);
  }
  
  def left(x: Integer, y: Integer, n:Integer): (Integer, Integer) = {
    return (x - n, y);
  }

  def right(x: Integer, y: Integer, n:Integer): (Integer, Integer) = {
    return (x + n, y);
  }

  def dist(movements: String): Integer = {
    val dirs = Seq('N', 'E', 'S', 'W');
    var curPos: (Integer, Integer) = (0, 0);
    
    var curDir = 0;
    for (movement <- movements.split(',')) {
      var m = movement.replaceAll("\\s", "");
      var dir = m(0);
      var steps = Integer.valueOf(m.drop(1));
      
      dir match {
        case 'R' => curDir = (curDir + 1) % 4;
        case 'L' => curDir = (curDir + 3) % 4;
      }

      curPos = dirs(curDir) match {
        case 'N' => up(curPos._1, curPos._2, steps);
        case 'E' => right(curPos._1, curPos._2, steps);
        case 'W' => left(curPos._1, curPos._2, steps);
        case 'S' => down(curPos._1, curPos._2, steps);
      }
    }
    return(Math.abs(curPos._1) + Math.abs(curPos._2));
  }
  def run() = {
    println(s"Distance: ${Main.dist(Main.readInp())}");
  }
}
