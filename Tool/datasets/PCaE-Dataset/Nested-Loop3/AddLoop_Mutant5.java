public class AddLoop_Mutant5 {
    // Class scope: focused on a simple additive looping example.

    // Note: This class demonstrates a simple additive loop.
    public static int AddLoop(int x, int y) {
        // Initialize the accumulator with the starting value x.
        int sum = x;
        if (y > 0) {
            // Positive input path: prepares to iterate downward.
            // Positive path: start from y and count down to 0.
            int n = y;
            while (n >= 0) {
                sum = sum + 1;
                n = n - 1;
            }
        } else {
            // Negative path: operate on absolute value of y.
            // Negative path: handle absolute value of y.
            int n = -y;
            while (n >= 0) {
                sum = sum - 1;
                n = n - 1;
            }
        }
        // Return the final accumulated sum.
        // Final value computed by the accumulation loop.
        return sum;
        // End of AddLoop computation.
    }
}