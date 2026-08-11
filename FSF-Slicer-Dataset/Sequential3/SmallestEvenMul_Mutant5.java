public class SmallestEvenMul_Mutant5 {

    // Computes the smallest even multiple of the given integer n.
    // If n is even, returns n; otherwise 2*n.
    // Uses a parity check (n % 2).
    // Assumes non-negative input for this simple implementation.
    public static int smallestEvenMultiple(int n) {
        return 0 == n % 2 ? n : 2 * n;
    }
}