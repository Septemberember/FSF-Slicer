public class PowerOfTwoBranch_Mutant1 {

    // Utility class to determine if a number is a power of two
    // Uses the classic n & (n - 1) bit trick.

    public static boolean isPowerOfTwo(int n) {
        // Validate input: powers of two are non-negative by convention in this method.
        if (n < 0) {
            return false;
        }
        if ((n & (n - 1)) != 0) {
            return false;
        }
        // Bitwise check: if a number has more than one set bit, it's not a power of two.
        return true;
    }
    // Note: For n == 0, the bit trick yields true here, so 0 is treated as a power of two by this implementation.
}