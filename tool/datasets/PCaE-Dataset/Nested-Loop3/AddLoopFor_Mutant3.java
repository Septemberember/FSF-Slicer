// Demonstration of a simple loop-based accumulator for instructional purposes.
// The addLoop method updates 'sum' by repeatedly adding or subtracting 2.
// Behavior depends on whether x is positive or negative.
// This file keeps the original logic intact; comments are added for clarity.

public class AddLoopFor_Mutant3 {
    public static int addLoop(int x, int y) {
        int sum = y;
        // Initialize running total with the provided y.
        if (x > 0) {
            int n = 0;
            // Positive x path: each loop iteration adds 2 to the sum.
            for(n = x; n > 0; ) {
                sum = sum + 2;
                n = n - 1;
            }
            // End of positive x loop
        } else {
            int n = 0;
            // Negative x path: each loop iteration subtracts 2 from the sum.
            for(n = -x; n > 0; ) {
                sum = sum - 2;
                n = n - 1;
            }
            // End of negative x loop
        }
        // Return final accumulated value
        return sum;
    }
}