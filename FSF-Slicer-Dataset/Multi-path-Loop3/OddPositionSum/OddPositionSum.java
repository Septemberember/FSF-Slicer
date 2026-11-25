public class OddPositionSum {
    public static int sumOddPositions(int count) {
        int stop = Math.min(count, 16);
        int sum = 0;
        for (int i = 1; i <= stop; i++) {
            if (i % 2 != 0) {
                sum += i;
            }
        }
        return sum;
    }
}
