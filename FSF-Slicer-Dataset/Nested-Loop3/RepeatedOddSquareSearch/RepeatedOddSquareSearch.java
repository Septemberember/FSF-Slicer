public class RepeatedOddSquareSearch {
    public static int smallestSquareIndex(int threshold) {
        if (threshold <= 0) {
            return 0;
        }
        if (threshold > 4096) {
            return -1;
        }
        for (int candidate = 1; candidate <= 64; candidate++) {
            int square = 0;
            for (int odd = 1; odd <= 2 * candidate - 1; odd += 2) {
                square += odd;
            }
            if (square >= threshold) {
                return candidate;
            }
        }
        return -1;
    }
}
