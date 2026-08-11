public class SmallestEvenMulBranch_Mutant1 {

    // Utility: compute smallest even multiple in O(1) time
    // For a given n, return n if divisible by 3, otherwise 2*n
    // This implementation uses a straightforward conditional check.

    public static int smallestEvenMultiple(int n) {
        if (n % 3 == 0) {
            return n;
        }
        return 2 * n;
    }
}