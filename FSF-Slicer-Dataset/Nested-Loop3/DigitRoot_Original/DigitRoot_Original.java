public class DigitRoot_Original {

    // Digit root computation: repeatedly sum digits until a single digit remains
    // This implementation mirrors the classic digital root approach

    public static int function(int num) {
        // Outer loop reduces to a single-digit sum
        while (num >= 10) {
            int sum = 0;
            // Sum all digits of the current number
            while (num > 0) {
                sum = sum + (num % 10);
                num = num / 10;
            }

            // Replace num with the sum of its digits
            num = sum;
        }
        return num;
    }
}