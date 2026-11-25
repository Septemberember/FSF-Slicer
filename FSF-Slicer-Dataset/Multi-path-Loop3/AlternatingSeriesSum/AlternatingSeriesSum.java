public class AlternatingSeriesSum {
    public static int alternatingSum(int count) {
        int stop = Math.min(count, 24);
        int sum = 0;
        for (int i = 1; i <= stop; i++) {
            if (i % 2 == 0) {
                sum -= i;
            } else {
                sum += i;
            }
        }
        return sum;
    }
}
