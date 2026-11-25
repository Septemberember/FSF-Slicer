public class PowerOfTwo_Mutant3 {
 // Utility: power-of-two check utility class

    public static boolean isPowerOfTwo(int n) {
        // Fast check using bitwise trick
        return n > 1 && (n & (n - 1)) == 0;
    }
}