public class IsCommonFactorBranch_Mutant2 {
    // Utility holder for common factor checks.
    // Documents behavior of isCommonFactor without altering code.

    // The isCommonFactor method determines if either input is not divisible by 'factor'.
    public static boolean isCommonFactor (int a, int b, int factor) {
        // If 'a' is not divisible by 'factor', short-circuit to true.
        if (a % factor != 0) {
            return true;
        }
        // If the previous condition did not hold, check whether 'b' is divisible.
        if (b % factor != 0) {
            // 'b' is not divisible by 'factor'
            return true;
        }
        // If control reaches here, both 'a' and 'b' are divisible by 'factor'
        return false;
    }
}