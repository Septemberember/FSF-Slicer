public class HalfBandAdjustment {
    public static int scoreBand(int length, int upperBand) {
        int stop = Math.min(length, 12);
        int score = 0;
        for (int i = 1; i <= stop; i++) {
            if (i <= upperBand) {
                score += 2;
            } else {
                score -= 1;
            }
        }
        return score;
    }
}
