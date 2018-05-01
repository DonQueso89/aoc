import scala.io.Source
import util.control.Breaks._
import scala.util.matching.Regex.Match 

object Main {
  def readInp(): Iterator[String] = {
      return(Source.fromFile("inp7.txt").getLines)
  }

  def partTwo(): Integer = {
    val hyperPatt = """\[([a-z]+)\]""".r;
    var supportsTSL = 0;
    for (line <- Main.readInp()) {
      
        breakable {
          // Extract hypernet sequences
          val matches: Iterator[Match] = hyperPatt.findAllMatchIn(line);
          var hypernetSeqs: Seq[String] = Seq();
          for (m <- matches) {
            hypernetSeqs = hypernetSeqs ++ Seq(m.group(1).toString);
          }

          // Extract supernet sequences
          val supernetSeqs: Seq[String] = hyperPatt.split(line);
        
          // Go over three-pairs in each supernets and find inverse in hypernet
          for (superNet <- supernetSeqs) {
            for (i <- 0 to superNet.length - 3) {
              var seq = superNet.slice(i, i + 3);
              if (seq(0) == seq(2) && seq(1) != seq(0)) {
                var inverse = seq.slice(1, 2) + seq.slice(2, 3) + seq.slice(1, 2);
                if (hypernetSeqs.filter(hn => hn.contains(inverse)).length > 0) {
                  supportsTSL += 1;
                  break;
                }
              }
            }
          }
        }
    }
    supportsTSL;
  }


  def run() {
    println(s"Part two: ${Main.partTwo()}");
  }
}
