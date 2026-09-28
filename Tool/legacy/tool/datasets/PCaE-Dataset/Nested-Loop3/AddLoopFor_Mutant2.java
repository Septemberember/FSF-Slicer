public class AddLoopFor_Mutant2 {
 // Simple control-flow example used for demonstrating a loop structure.
 // This class documents intent without altering the existing logic.
 // Natural continuation of the original implementation.

    public static int addLoop(int x, int y) {
 // Method addLoop computes a sum by incrementing or decrementing based on x.
        int sum = y;
 // Initialize accumulator with input value y.
        if (x > 0) {
 // Positive x branch: accumulate upward with step of 1.
            int n = 0;
 // Local loop counter for the positive branch.
            for(n = x; n > 0; ) {
 // Loop condition: continue while n remains positive.
                sum = sum + 1;
                n = n - 2;
            }
 // End of the positive x branch.
        } else {
 // Negative or zero x branch: accumulate downward with subtraction.
            int n = 0;
 // Local loop counter for the negative branch.
            for(n = -x; n > 0; ) {
 // Loop condition: continue while n remains positive.
                sum = sum - 1;
                n = n - 2;
            }
 // End of the negative x branch.
        }
 // Return the computed sum.
        return sum;
 // End of addLoop method.
    }
 // End of class AddLoopFor_Mutant2.
}