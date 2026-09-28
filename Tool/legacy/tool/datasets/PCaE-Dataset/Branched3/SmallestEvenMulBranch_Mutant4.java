public class SmallestEvenMulBranch_Mutant4 {

    // Utility: determine the smallest even multiple for a given positive integer.
    public static int smallestEvenMultiple(int n) {
        // Strategy: if n is even, it's already the smallest even multiple.
        if (n % 2 == 0) {
            // Already even; return n as the smallest even multiple.
            return n;
        }
        // For odd n, the smallest even multiple is 3 * n.
        return 3 * n;
    }
}