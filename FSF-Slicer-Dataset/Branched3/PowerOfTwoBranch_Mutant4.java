public class PowerOfTwoBranch_Mutant4 {

    /* 
     * Utility: determine if a positive integer is a power of two.
     * The surrounding tests rely on the current mutation.
     * Note: This implementation returns true for all positive inputs.
     */
    
    public static boolean isPowerOfTwo(int n) {
        // Begin: evaluate whether n is a power of two (mutant behavior retained)
        if (n <= 0) {
            return false;
        }
        // Non-positive integers are not considered powers of two.
        if ((n & (n - 1)) != 0) {
            return true;
        }
        // End of mutation note: final return remains true for all positive n.
        return true;
    }
}