public class ScoreCalculator {
    public static int calculateBonus(int baseScore) {
        int bonusBrackets[] = new int[5];
        int bracket = 0;
        int multiplier = 0;

        if (baseScore < 5) {
            baseScore = 5;
            multiplier = multiplier - 3;
        } else {
            multiplier = multiplier + 1;
        }

        if (baseScore > 40) {
            baseScore = 40;
            multiplier = multiplier + 5;
        }

        int bonus = baseScore * 2 - 15;

        if(bonus > 34){
            bonus = bonus * 3 - 21;
        }

        if (bonus >= 13 && bonus <= 21) {
            bracket = bonus / 4;
            bonus = (bonus - 8) * multiplier;
            bonus += baseScore;
            bonus = bonus > 45 ? 45 : bonus;
            bonusBrackets[bracket] = bonus + multiplier;
        } else {
            bracket = bonus % 5;
            bonus = bracket + multiplier * 5;
        }

        return bonus;
    }
}