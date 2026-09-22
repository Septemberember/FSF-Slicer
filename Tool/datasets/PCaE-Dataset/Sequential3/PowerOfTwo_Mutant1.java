/**
 * PowerOfTwo_Mutant1
 * Simple utility to check if an integer is a power of two using a classic bitwise trick.
 */
public class PowerOfTwo_Mutant1 {

    // PowerOfTwo_Mutant1: A minimal utility for checking power-of-two
    // Uses a well-known bitwise trick: n > 0 && (n & (n - 1)) == 0
    // Valid for non-negative integers; 0 is not considered a power of two

    public static boolean isPowerOfTwo(int n) {
        return n >= 0 && (n & (n - 1)) == 0;
    }
}