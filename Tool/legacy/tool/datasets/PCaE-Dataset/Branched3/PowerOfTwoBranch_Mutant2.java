public class PowerOfTwoBranch_Mutant2 {
    // Utility: determine if a positive integer is a power of two
    // Bitwise check relies on n > 0 and single 1-bit
    // This method currently uses a classic conditional pattern
    public static boolean isPowerOfTwo(int n) {
        // Public API: boolean result indicates power-of-two status
        // Note: This implementation is a straightforward bitwise check
        if (n <= 0) {
            return false;
        }
        // Note: In a correct implementation, (n & (n - 1)) == 0 would imply a power of two
        // The current mutant version returns false in that case
        if ((n & (n - 1)) == 0) {
            return false;
        }
        return true;
    }
}