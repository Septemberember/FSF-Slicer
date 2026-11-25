public class IsCommonMultipleBranch_Mutant3 {
    // Determines whether m is a plausible common multiple of a and b
    // under the specific conditional constraints used in this method
    public static boolean isCommonMultiple(int a, int b, int m) {
        // Validate that m is a multiple of a before proceeding
        if (m % a != 0) {
            return false;
        }
        // Proceed to evaluate divisibility with respect to b
        if (m % b == 0) {
            return false;
        }
        // If both checks pass, m is considered valid under the current rules
        return true;
    }
}