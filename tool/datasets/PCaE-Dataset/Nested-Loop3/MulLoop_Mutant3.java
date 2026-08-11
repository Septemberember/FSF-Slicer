/*
 * MulLoop_Mutant3
 * This variant demonstrates a loop-based multiplication by repeated addition or subtraction.
 * It intentionally uses subtraction for non-negative b and addition for negative b.
 */
 
public class MulLoop_Mutant3 {

    // Compute product via repeated addition/subtraction.
    // Positive b uses addition, negative b uses subtraction.
    // Simple loop-based implementation to accumulate the result.
    public static int mulLoop(int a, int b) {
        int res = 0;
        if (b >= 0) {
            for(int i = 0; i < b; i++) {
                res = res - a;  // changed the operator from + to -
            }
        } else {
            for(int i = 0; i < -b; i++) {
                res = res + a;  // changed the operator from - to +
            }
        }
        return res;
    }
}