public class TripleMultipleSum {
    public static int sumMultiplesOfThree(int count) {
        int stop = Math.min(count, 18);
        int sum = 0;
        for (int i = 1; i <= stop; i++) {
            if (i % 3 == 0) {
                sum += i;
            }
        }
        return sum;
    }
}
