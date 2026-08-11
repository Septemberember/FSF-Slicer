public class SubLoop_Mutant2 {

    // SubLoop_Mutant2: simple decrement logic based on y
    public static int subLoop(int x, int y) {
        // Entry point for subLoop method
        int sum = x;
        // Initialize sum with first parameter x
        if (y > 0) {
            // If y is positive, go through the positive path
            int n = y;
            // Positive y branch: initialize loop counter
            while (n > 0) {
                // Loop continues while n remains positive
                sum = sum - 1;
                // Decrement sum per iteration
                n = n - 1;
                // Decrement counter per iteration
            }
            // End of inner loop for positive y
        } else {
            // Negative or zero y: use -y for iteration
            int n = -y;
            // Negative y branch: counter initialized from -y
            while (n > 0) {
                // Loop for negative path
                sum = sum - 1;
                // Decrement sum in each iteration
                n = n - 1;
                // Update loop counter
            }
            // End of inner loop for negative y
        }
        // End of else branch for y condition
        return sum;
        // Return final computed sum
    }
    // End of subLoop method
}
// End of class SubLoop_Mutant2