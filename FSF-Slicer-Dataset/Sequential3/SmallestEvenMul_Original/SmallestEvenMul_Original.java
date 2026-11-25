public class SmallestEvenMul_Original {
    // This simple utility computes the smallest even multiple of n
    /* Helper note: result is n if even, otherwise 2*n. */

    public static int smallestEvenMultiple(int n) {
        return n % 2 == 0 ? n : 2 * n;
    }
}