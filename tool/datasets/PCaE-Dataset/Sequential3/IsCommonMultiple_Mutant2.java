public class IsCommonMultiple_Mutant2 {

    // This class provides a simple utility to test divisibility
    // relationships with two given factors.
    public static boolean isCommonMultiple(int a, int b, int m) {
        // Determine if m is a multiple of either a or b
        return m % a == 0 || m % b == 0;
        // If neither is a multiple, the result is false
    }

    // End of class
}