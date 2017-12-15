import java.util.*;

public class Deck {
    List<Card> cards = new ArrayList<>(); //stores the deck of cards
    static Deck currentDeck = null; //singleton Design Pattern

    public Deck() {
        if (currentDeck == null) {
            for (int i = 0; i < 4; i++) {
                for (int j = 1; j < 14; j++) {
                    cards.add(new Card(j, i));
                }
            }
            shuffleDeck();
        }
    }

    public static Deck getInstance() {
        if (currentDeck == null) {
            currentDeck = new Deck();
        }
        return currentDeck;
    }

    public void shuffleDeck() {
        List<Card> newRandCards = new ArrayList<>();
        while (cards.size() > 0) {
            newRandCards.add(this.takeRandomCard());
        }
        this.cards = new ArrayList<Card>(newRandCards);
    }

    public Card peekCard() {
        return cards.get(cards.size()-1);
    }

    private Card throwCard(int index) {
        Card popCard = cards.get(index);
        cards.remove(index);
        return popCard;
    }

    public Card takeTopCard() {
        return throwCard(cards.size()-1);
    }

    public Card takeRandomCard() {
        Random rand = new Random(System.nanoTime());
        int n = rand.nextInt(cards.size());
        return throwCard(n);
    }
}
