
import java.lang.*;
import java.util.*;

public class GameClass {
    private ArrayList<Player> players = new ArrayList<>();
    private Player winner;

    public ArrayList<Player> getPlayers() {
        return players;
    }

    public int numPlayers() {
        return players.size();
    }

    public Player winner() {
        return winner;
    }

    public GameClass (String command) {
        Deck texasHigh = new Deck();
        Dealer house = new Dealer(texasHigh, 2, false);
        Player me = house.allowEntry("me", 2, texasHigh);
        players.add(house);
        players.add(me);

        house.hitPlayer(texasHigh);
        me.hitPlayer(texasHigh);
        house.hitPlayer(texasHigh);

         while (!me.hasFolded()) {
             me.hitPlayer(texasHigh);
             house.requestFold();
         }

         winner = house.whoWon(me);

        System.out.println(winner);
        }
    }
}
