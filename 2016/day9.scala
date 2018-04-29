import scala.io.Source
import util.control.Breaks._

object Main {
  def readInp(): String = {
      return(Source.fromFile("inp9.txt").getLines.mkString)
  }

  def getDecompressedSize(compressed: String, multiplier: Integer=1): Long = {
    /*
     * Recursively get decompressed size of data
     */
    if (compressed.contains('(')) { // Recursive case
      val patt = """(\d+)x(\d+)""".r
      var decompressInfo = "";
      var result: Long = 0;
      var i = 0;
      do {
        var char = compressed(i);
        breakable {
          char match {
            case char if "ABCDEFGHIJKLMNOPQRSTUVWXYZ".contains(char) => {
              result += 1;
              i += 1;
              break;
            }
            case '(' => { // start of decomp info
              i += 1;
              break;
            }
            case ')' => { // end of decomp info
              val patt(size, reps) = decompressInfo;
              result += getDecompressedSize(
                compressed.slice(
                  i + 1, 
                  i + 1 + Integer.valueOf(size)
                ), 
                multiplier=Integer.valueOf(reps)
              );
              decompressInfo = "";
              i += (Integer.valueOf(size) + 1);
              break;
            }
            case char if "0123456789x".contains(char) => {
              decompressInfo += char;
              i += 1;
              break;
            }
          }
        }
      } while (i < compressed.length)
      return result * multiplier;
    } else { // Base case
      return(compressed.length * multiplier)
    }
  }

  def run() {
    val result: Long = Main.getDecompressedSize(Main.readInp());
    println(s"Day 2 part 2: ${result}");
  }
}
