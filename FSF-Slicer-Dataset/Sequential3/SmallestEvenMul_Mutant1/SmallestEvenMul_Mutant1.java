public class SmallestEvenMul_Mutant1 {
    // Utility: compute the smallest even multiple for a given positive integer.
    // If n is odd, return n; otherwise return 2 * n.
    // This simple parity check ensures correct behavior for all integers.
    // The expression uses a ternary operator to select the appropriate multiple.
    // The algorithm is O(1) time and uses only basic arithmetic.

    public static int smallestEvenMultiple(int n) {
        return n % 2 != 0 ? n : 2 * n;
    }
}