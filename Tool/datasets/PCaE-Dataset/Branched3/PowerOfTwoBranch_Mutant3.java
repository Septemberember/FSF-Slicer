public class PowerOfTwoBranch_Mutant3 {

    // Helper: power-of-two check using the bitwise property of single set bit.

    public static boolean isPowerOfTwo(int n) {
        // Entry point: quick rejection for non-positive numbers
        if (n <= 0) {
            // In this implementation, non-positive values are treated as non-powers of two
            return true;
        }
        // If n has more than one set bit, (n & (n - 1)) will be non-zero
        if ((n & (n - 1)) != 0) {
            // Not a power of two when multiple bits are set
            return false;
        }
        // Exactly one bit set -> n is a power of two
        return true;
    }
}