import scala.io.Source
import util.control.Breaks._

object Main {
  def readInp(): Iterator[String] = {
      return(Source.fromFile("inp10.txt").getLines)
  }

  def resolveMicrochips(instructions: Iterator[String]): (Integer, Integer) = {
      // Set up state
      // bot -> initial value(s)
      val bots = collection.mutable.Map[Integer, Seq[Integer]]();

      // bot -> Seq(low, high)
      val transactions = collection.mutable.Map[Integer, Seq[String]]();

      val outputs = collection.mutable.Map[Integer, Seq[Integer]]();

      var result = 0;

      // Handout microchips. Keep transactions.
      for (instruction <- instructions) {
        if (instruction.contains("goes")) {
          val payload = instruction.split(" ");
          val microchip = Integer.valueOf(payload(1));
          val receiver = Integer.valueOf(payload(5));

          bots.get(receiver) match {
            case Some(microchips: Seq[Integer]) => bots.update(receiver, microchips :+ microchip);
            case None => bots.update(receiver, Seq(microchip));
          }
        } else {
          // 1 transaction per bot
          val payload = instruction.split(" ");
          val low: (String, String) = (payload(5), payload(6));
          val high: (String, String) = (payload(10), payload(11));
          val bot: Integer = Integer.valueOf(payload(1));
          transactions.update(bot, Seq(s"${low._1(0)}${low._2}", s"${high._1(0)}${high._2}"));
        }
      }
      
      // Execute next transaction until we hit the case
      var nextBot: (Integer, Seq[Integer]) = bots.filter(x => x._2.length == 2).toSeq(0);
      var nextTransaction = transactions.remove(nextBot._1).toSeq(0);
      while (true) {
        val values = nextBot._2.sorted;
        val botDestination: Seq[Boolean] = nextTransaction.map(x => x(0) == 'b');
        val destinations: Seq[Integer] = nextTransaction.map(x => Integer.valueOf(x.slice(1, x.length)));
        if (values == List(61, 17) || values == List(17, 61)) {
          result = nextBot._1;
        }
        val sender = nextBot._1;
        for (i <- 0 to 1) {
          val receiver = destinations(i);
          val microchip = values(i);
          if (botDestination(i)) {
            // Add to receiver 
            bots.get(receiver) match {
              case Some(microchips: Seq[Integer]) => bots.update(receiver, microchips :+ microchip);
              case None => bots.update(receiver, Seq(microchip));
            }
          } else {
            outputs.get(receiver) match {
              case Some(microchips: Seq[Integer]) => outputs.update(receiver, microchips :+ microchip);
              case None => outputs.update(receiver, Seq(microchip));
            }
          }
        }
        // Remove from sender
        bots.update(sender, Seq[Integer]());
        if (transactions.toSeq.length > 0) {
          nextBot = bots.filter(x => x._2.length == 2).toSeq(0);
          nextTransaction = transactions.remove(nextBot._1).toSeq(0);
        } else {
          return((result, outputs.get(0).get(0) * outputs.get(1).get(0) * outputs.get(2).get(0)));
        }
      }
      (-1, - 1);
    }

  def run() {
    val result: (Integer, Integer) = Main.resolveMicrochips(Main.readInp());
    println(s"Day 10 part 1: ${result._1} part 2: ${result._2}");
  }
}
