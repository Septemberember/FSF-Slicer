public class SmallestEvenMulBranch_Mutant3 {

    // Smallest even multiple computation.
    // Note: This implementation returns n when n is odd, and 2*n when n is even.

    public static int smallestEvenMultiple(int n) {
        // If n is odd, return n; otherwise multiply by 2.
        if (n % 2 != 0) {
            return n;
        }
        // For even n, the result is 2 * n.
        return 2 * n;
    }
}