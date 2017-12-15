import java.util.*;
import java.lang.*;

public class DeepLearner {
    HashMap<Integer, ArrayList<Integer>> deepBelief = new HashMap<>();

    public DeepLearner() {
        for (int i = 4; i < 23; i++) {
            ArrayList<Integer> vals = new ArrayList<>();
            vals.add(0);
            vals.add(0);
            vals.add(0);
            vals.add(0);
            deepBelief.put(i, vals);
        }
    }

    public void buildBelief() {
        for (int i = 0; i < 300000; i++) {
            GameClass game = new GameClass(null);
            int score = game.getInitialScore();
            ArrayList<Integer> probabilities = deepBelief.get(score);
            boolean tookExtraCard = game.houseTookAnother();
            int index = 0;

            if (tookExtraCard) {
                index = 1;
                probabilities.set(3, probabilities.get(3) + 1);
            }
            else {
                index = 0;
                probabilities.set(2, probabilities.get(2) + 1);
            }

            if (game.winner().getName().equals("House")) {
                probabilities.set(index, probabilities.get(index) + 1);
            }
        }
    }

    public boolean getAnotherCard(int score) {
        ArrayList<Integer> probabilities = deepBelief.get(score);
        if (probabilities.get(1) > probabilities.get(0)) return true;
        else return false;
    }

}
