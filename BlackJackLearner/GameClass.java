import java.lang.*;
import java.util.*;

public class GameClass {
    private ArrayList<Player> players = new ArrayList<>();
    private Player winner;
    private boolean tookAnother;
    private int initialScore;

    public int getInitialScore() { return initialScore;}
    public boolean houseTookAnother() {return tookAnother;}

    public ArrayList<Player> getPlayers() {
        return players;
    }

    public int numPlayers() {
        return players.size();
    }

    public Player winner() {
        return winner;
    }

    public GameClass (DeepLearner myChamp) {
        Deck texasHigh = new Deck();
        Dealer house = new Dealer(texasHigh, 2, false);
        Player me = house.allowEntry("me", 2, texasHigh);
        players.add(house);
        players.add(me);

        house.hitPlayer(texasHigh);
        me.hitPlayer(texasHigh);
        house.hitPlayer(texasHigh);

        initialScore = house.cardScore();
         while (!me.hasFolded()) {
             me.hitPlayer(texasHigh);
             me.requestFold();
         }

        while (!house.hasFolded()) {
            house.hitPlayer(texasHigh);
            house.requestFold();
        }

         if (house.cards.size() > 2) {
             tookAnother = true;
         } else tookAnother = false;

         winner = house.whoWon(me);

         System.out.println(winner.getName());
        }
    }