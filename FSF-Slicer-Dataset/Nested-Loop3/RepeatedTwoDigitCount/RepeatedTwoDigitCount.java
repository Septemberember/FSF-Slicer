public class RepeatedTwoDigitCount {
    public static int count(int limit) {
        int count = 0;
        for (int number = 10; number <= Math.min(limit, 99); number++) {
            int rightDigit = number % 10;
            int equalDigits = 0;
            for (int digits = number; digits != 0; digits /= 10) {
                if (digits % 10 == rightDigit) {
                    equalDigits++;
                }
            }
            if (equalDigits == 2) {
                count++;
            }
        }
        return count;
    }
}
