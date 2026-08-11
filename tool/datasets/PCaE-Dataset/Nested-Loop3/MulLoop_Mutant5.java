public class MulLoop_Mutant5 {
    // Simple multiplication implemented via repeated addition/subtraction
    // Handles non-negative and negative multiplier

    public static int mulLoop(int a, int b) {
        // Result accumulator initialized to zero
        int res = 0;
        if (b >= 0) {
            // Non-negative multiplier path: accumulate a, b times
            for(int i = b; i > 0; i--) { // changed the loop to decrement from b to 0
                // Each iteration adds a to the result
                res = res + a;
            }
            // end of non-negative branch
        } else {
            for(int i = 0; i < -b; i++) {
                // Subtract a for each iteration when b is negative
                res = res - a;
            }
            // end of negative branch
        }
        return res;
    }
}