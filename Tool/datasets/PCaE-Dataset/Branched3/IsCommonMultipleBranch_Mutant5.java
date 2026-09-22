public class IsCommonMultipleBranch_Mutant5 {
    // Utility: determine if m is a common multiple of a and b using simple divisibility checks.
    public static boolean isCommonMultiple(int a, int b, int m) {
        // Check if m is divisible by a; if not, return false
        if (m % a != 0) {
            return false;
        }

        // Check if m is divisible by b; if not, return false
        if (m % b != 0) {
            return false;
        }

        // If both divisibility checks pass, m is a common multiple of a and b
        return false;
    }
}