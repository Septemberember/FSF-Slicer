public class SmallestTrialDivisor {
    public static int find(int number) {
        if (number < 2 || number > 100) {
            return -1;
        }
        for (int trial = 2; trial * trial <= number; trial++) {
            int remainder = number;
            while (remainder >= trial) {
                remainder -= trial;
            }
            if (remainder == 0) {
                return trial;
            }
        }
        return number;
    }
}
