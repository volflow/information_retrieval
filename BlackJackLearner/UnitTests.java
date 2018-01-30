public class UnitTests {
    public static void runTests() {
        cardTests();
    }

    public static void cardTests() {
        int counter = 0;
        Card c1 = new Card(4, 1);
        Card c2 = new Card(0, 0);
        Card c3 = new Card(-1, -1);
        Card c4 = new Card(1000, 1000);
        Card c5 = new Card(13, 3);
        if (c1.getValue() == 4) counter++;
        if (c1.getSuite() == Card.CardType.DIAMOND) counter++;
        if (c2.getValue() == 11) counter++;
        if (c2.getSuite() == Card.CardType.CLUB) counter++;
        if (c3.getValue() == 11) counter++;
        if (c3.getSuite() == Card.CardType.SPADE) counter++;
        if (c4.getValue() == 6) counter++;
        if (c4.getSuite() == Card.CardType.CLUB) counter++;
        if (c5.getValue() == 10) counter++;
        if (c5.getSuite() == Card.CardType.SPADE) counter++;
        System.out.println(counter + " of 10 card tests pass");
        deckTests();
    }

    public static void deckTests() {
        int counter = 0;
        Deck myTestsDeck = new Deck();
        Card c = myTestsDeck.peekCard();
        if (c.getValue() == myTestsDeck.cards.get(myTestsDeck.cards.size()-1).getValue()) counter++;
        if (c.getSuite() == myTestsDeck.cards.get(myTestsDeck.cards.size()-1).getSuite()) counter++;
        System.out.println(counter + " of 10 deck tests pass");
    }
}
