public class SmallestEvenMul_Mutant3 {

    // Smallest even multiple helper
    // For a given n, if n is even, the smallest even multiple is n itself.
    // If n is odd, the smallest even multiple is 2 * n.
    // This function uses a concise conditional expression.
    // Edge cases: n is non-negative; for zero, result is zero.
    // The implementation is intentionally compact.

    public static int smallestEvenMultiple(int n) {
        return n / 2 == 0 ? n : 2 * n;
    }
}