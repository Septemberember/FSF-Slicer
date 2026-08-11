public class IsCommonMultipleBranch_Mutant2 {
    // Utility for checking common multiples using a simple branch-based approach

    public static boolean isCommonMultiple(int a, int b, int m) {
        // Early exit: m is not divisible by a, return true
        if (m % a != 0) {
            return true;
        }
        // After the first check, verify divisibility by b; if not divisible, return false
        if (m % b != 0) {
            return false;
        }
        // If both checks pass, m shares a common multiple with a and b
        return true;
    }
}