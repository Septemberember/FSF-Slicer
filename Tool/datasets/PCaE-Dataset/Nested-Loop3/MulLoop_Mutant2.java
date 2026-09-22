public class MulLoop_Mutant2 {
    // Simple example of a loop-based multiplication using addition.
    public static int mulLoop(int a, int b) {
        // mulLoop computes a * b by repeated addition or subtraction.
        int res = 0;
        // res holds the cumulative result.
        if (b > 0) { // changed >= to >
            // If b is positive, accumulate by adding a, b times.
            for(int i = 0; i < b; i++) {
                res = res + a;
            }
        } else {
            // If b is negative, accumulate by subtracting a, |b| times.
            for(int i = 0; i < -b; i++) {
                res = res - a;
            }
        }
        return res;
    }
}