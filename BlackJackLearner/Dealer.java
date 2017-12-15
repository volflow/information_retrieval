import java.util.*;
import java.lang.*;

public class Dealer extends Player {
    private boolean strictRules;
    List<Player> table = new ArrayList<>();
    private boolean folded;

    public Dealer(Deck deck, int numCards, boolean strictRules) {
        super("House", numCards, deck);
        table.add(this);
        this.strictRules = strictRules;
    }

    public Player allowEntry(String name, int cardsRequest, Deck deck) {
        if (strictRules) return new Player(name, 2, deck);
        else return new Player(name, cardsRequest, deck);
    }

    public Player whoWon(Player p1) {
        if (this.cardScore() > 21) {
            if (p1.cardScore() > 21) {
                return (new Player("No-one wins", 2, (new Deck())));
            } else {
                return p1;
            }
        } else {
            if (p1.cardScore() > 21) {
                return this;
            }
        }
        if (this.cardScore() > p1.cardScore()) {
            return this;
        }
        else if (p1.cardScore() > this.cardScore()) {
            return p1;

        }
        return this;
    }

    public void serveCard(Player p1, Deck deck) {
        p1.hitPlayer(deck);
    }

    public void requestFold(DeepLearner deep) {
        if (deep == null) {
            if ( (((new Random(System.currentTimeMillis())).nextInt(2) % 2) == 0)) {
                this.folded = true;
            }
        } else {
            if (!deep.getAnotherCard(this.cardScore())) this.folded = true;
        }
    }

}
