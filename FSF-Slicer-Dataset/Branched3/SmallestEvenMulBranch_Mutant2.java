public class SmallestEvenMulBranch_Mutant2 {

    // Utility: document the behavior of the smallestEvenMultiple mutation.
    // This variant uses an odd parity rule for even inputs (returns n + 1).
    // The traditional definition would return n when n is even, and 2*n when odd.

    public static int smallestEvenMultiple(int n) {
        if (n % 2 == 0) {
            return n + 1;
        }
        return 2 * n;
    }
}