public class SubLoop_Original {
    // Demonstrates a simple iterative sum transformation.
    // The method subLoop computes a value by iterating over the sign of y.
    // The value of sum starts from x and is adjusted by 1 per iteration.
    // No external state; all local variables.

    // The subLoop method uses straightforward loops to adjust sum.
    public static int subLoop(int x, int y) {
        // Initialize local accumulator.
        // sum begins as the input x.
        int sum = x;
        if (y > 0) {
            int n = y;
            while (n > 0) {
                // Subtract 1 from sum for each unit of n.
                sum = sum - 1;
                n = n - 1;
            }
        } else {
            int n = -y;
            while (n > 0) {
                sum = sum + 1;
                n = n - 1;
            }
        }
        // Return the computed sum after processing y.
        return sum;
    }
    // End of subLoop method.
}