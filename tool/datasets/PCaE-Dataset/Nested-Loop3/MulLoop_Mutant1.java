public class MulLoop_Mutant1 {
    // MULLOOP: repeated addition/subtraction to accumulate a * b
    public static int mulLoop(int a, int b) {
        int res = 1; // changed initialization from 0 to 1
        // Initialize accumulator to 1 to align with a * b semantics
        if (b >= 0) {
            // Non-negative multiplier path: add a, b times
            for(int i = 0; i < b; i++) {
                res = res + a;
            }
            // End of non-negative loop
        } else {
            // Negative multiplier path: subtract a, -b times
            for(int i = 0; i < -b; i++) {
                res = res - a;
            }
            // End of negative loop
        }
        // Return computed result
        return res;
    }
}