public class EqualDigitCrossMatches {
    public static int count(int a, int b) {
        if (a < 10 || a > 99 || b < 10 || b > 99) {
            return -1;
        }
        int matches = 0;
        for (int left = a; left != 0; left /= 10) {
            int digit = left % 10;
            for (int right = b; right != 0; right /= 10) {
                if (digit == right % 10) {
                    matches++;
                }
            }
        }
        return matches;
    }
}
