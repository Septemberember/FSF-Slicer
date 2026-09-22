public class SubLoop_Mutant5 {
    // This class provides a small utility method used in loop-based computation
    public static int subLoop(int x, int y) {
        // Initialize the accumulator with the initial value
        int sum = x;
        // Branch based on the sign of y to determine loop behavior
        if (y > 0) {
            // When y is positive, perform a decrement loop
            int n = 0;
            while (n > 0) {
                sum = sum - 1;
                n = n - 1;
            }
        } else {
            // When y is non-positive, perform an increment loop
            int n = -y;
            while (n > 0) {
                sum = sum + 1;
                n = n - 1;
            }
        }
        // Return the computed sum
        return sum;
    }
}