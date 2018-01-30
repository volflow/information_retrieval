import java.lang.*;

public class Card {
    public enum CardType {
        CLUB(0), DIAMOND(1), HEART(2), SPADE(3);
        private final int theCard;

        CardType(int inCard) {
            this.theCard = inCard;
        }

        public static CardType getType(int card) {
            card = card % 4;
            if (card == 0) return CLUB;
            if (card == 1) return DIAMOND;
            if (card == 2) return HEART;
            else return SPADE;

        }
    }

    public static int scoreSystem (int cardIndex){
        if (cardIndex == 0) cardIndex++;
        else cardIndex = (cardIndex % 14); //ensure value is between 1 and 13 in case of user input error
        switch(cardIndex) {
            case 1 : return 11; //Ace is worth 11 (as a max)
            case 11 : return 10; //K, Q, J worth 10 each
            case 12 : return 10;
            case 13 : return 10;
            default : return cardIndex; //if no special cards present, just return the card value
        }
    }

    public String cardPrintString() {
        switch(this.value) {
            case 1:
                return "Ace"; //Ace is worth 11 (as a max)
            case 11:
                return "Jack"; //K, Q, J worth 10 each
            case 12:
                return "Queen";
            case 13:
                return "King";
            default:
                return Integer.toString(this.value); //if no special cards present, just return the card value
        }
    }

    private final int value;
    private final CardType suite;

    private int bound(int score) {
        if (score < 1) return 1;
        if (score > 13) return (score % 14);
        return score;
    }

    public Card(int cardIndex, int suite) {
        this.value = bound(cardIndex);
        this.suite = CardType.getType(suite);
    }

    public String printCard() {
        return (this.cardPrintString() + " of " + suite);
    }

    public int getValue() {
        return scoreSystem(this.value);
    }

    public CardType getSuite() {
        return this.suite;
    }
}