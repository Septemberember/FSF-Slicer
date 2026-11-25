public class DigitSumPassCount {
    public static int count(int number) {
        if (number < 0 || number > 999) {
            return -1;
        }
        int passes = 0;
        while (number >= 10) {
            int sum = 0;
            while (number != 0) {
                sum += number % 10;
                number /= 10;
            }
            number = sum;
            passes++;
        }
        return passes;
    }
}
