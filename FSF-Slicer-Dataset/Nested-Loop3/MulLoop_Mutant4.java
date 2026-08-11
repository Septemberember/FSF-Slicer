public class MulLoop_Mutant4 {
    // MulLoop_Mutant4: a naive multiplication using repeated addition.
    // The implementation uses a loop to accumulate the product.
    // Note: the loop increments the index by 2 for demonstration.
    // Keeping code simple and readable.

    public static int mulLoop(int a, int b) {
        int res = 0;
        // initialize result to zero
        // prepare for accumulation logic
        if (b >= 0) {
            for(int i = 0; i < b; i=i+2) { // increased the counter by 2
                res = res + a;
            }
        } else {
            for(int i = 0; i < -b; i=i+2) { // increased the counter by 2
                res = res - a;
            }
        }
        return res;
    }
}