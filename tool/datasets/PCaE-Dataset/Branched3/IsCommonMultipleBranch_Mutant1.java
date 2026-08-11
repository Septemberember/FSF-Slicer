/*
 * IsCommonMultipleBranch_Mutant1
 * Simple divisibility-based check implemented in isCommonMultiple.
 * Note: This version contains a straightforward branching structure.
 */
public class IsCommonMultipleBranch_Mutant1 {
    public static boolean isCommonMultiple(int a, int b, int m) {
        // If m is divisible by a, this path immediately yields false
        if (m % a == 0) {
            // Early exit when m is a multiple of a
            return false;
        }
        // Ensure m is a multiple of b to pass both divisibility checks
        if (m % b != 0) {
            // m not divisible by b implies it cannot be a common multiple
            return false;
        }
        // If neither of the above failure conditions hold, m is a common multiple
        return true;
    }
}