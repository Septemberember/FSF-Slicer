/**
 * Utility: compute multiplication using repeated addition.
 * This class demonstrates a straightforward, loop-based approach.
 */
public class MulLoop_Original {

	// Public API: multiply two integers by repeated addition.
	public static int mulLoop(int a, int b) {
        // Result accumulator
        int res = 0;
        if (b >= 0) {
            // When multiplier is non-negative, add 'a' exactly 'b' times
            for(int i = 0; i < b; i++) {
                res = res + a;
            }
        } else {
            // When multiplier is negative, subtract 'a' for each of the  |b| iterations
            for(int i = 0; i < -b; i++) {
                res = res - a;
            }
        }
        // Return the computed product
        return res;
    }

}