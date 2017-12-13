import java.util.*;
import java.lang.*;

public class Player {
    private int cardVal;
    private boolean busted;
    private final String name;
    private List<Card> cards;
    private boolean folded;
    private boolean iWon = false;

    public Player(Deck deck) {
        this("Guest", 2, deck);
    }

    public Player(String name, int numCardOption, Deck deck) {
        this.cardVal = 0;
        this.busted = false;
        this.name = name;
        this.cards = new ArrayList<Card>();
        for (int i = 0; i < numCardOption; i++) {
            this.cards.add(deck.takeTopCard());
        }
    }

    public int cardNum() {
        return (cards.size());
    }

    public int cardScore() {
        return this.cardVal;
    }

    public void printAllCards() {
        for (Card c : cards) {
            System.out.println(c.printCard());
        }
    }

    private void runGame(int overall) {
        this.cardVal = overall;
        if (overall > 21) {
            this.busted = true;
            this.requestFold();
        }
        else if (overall == 21) {
            this.requestFold();
            iWon = true;
        }
    }

    public int hitPlayer(Deck deck) {
        Card c = deck.takeTopCard();
        cards.add(c);
        int overall = this.cardVal + c.getValue();
        this.runGame(overall);
        return this.cardVal;
    }

    public boolean hasFolded() {
        return this.folded;
    }

    public void requestFold() {
        if (!this.hasFolded()) {
            Scanner in = new Scanner(System.in);
            String response = in.nextLine();
            if (response.equals("y")) this.folded = true;
        }
    }
}