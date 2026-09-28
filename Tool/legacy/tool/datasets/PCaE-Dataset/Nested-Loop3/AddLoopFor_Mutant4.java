// Utility class for demonstrating a simple loop-based calculation.
// This method operates purely on its input values x and y.
public class AddLoopFor_Mutant4 {
    public static int addLoop(int x, int y) {
        int sum = y;
        // Positive-x branch: iterates while x > 0, updating sum and n.
        if (x > 0) {
            int n = 0;
            // Initialize loop counter n from x, counting down.
            for(n = x; n > 0; ) {
                // Decrement sum and loop counter in each iteration.
                sum = sum - 1;
                n = n - 1;
            }
            // End of the positive-x branch when the for-loop completes.
        } else {
            int n = 0;
            // Negative-or-zero-x branch: accumulate when x is non-positive.
            for(n = -x; n > 0; ) {
                // Decrement loop counter and adjust sum accordingly.
                sum = sum + 1;
                n = n - 1;
            }
            // End of the negative-x branch.
        }
        // After both branches, the computed sum is returned.
        return sum;
        // Return point: sum is returned to the caller.
    }
    // End of addLoop method.
}
// End of class AddLoopFor_Mutant4.