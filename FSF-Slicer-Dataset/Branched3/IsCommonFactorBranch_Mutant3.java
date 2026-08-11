public class IsCommonFactorBranch_Mutant3 {

    // Core logic: check that both inputs leave a remainder of 1 when divided by factor
    public static boolean isCommonFactor (int a, int b, int factor) {
        if (a % factor != 1) {
            return false;
        }

        // Validate second input against the same remainder condition
        if (b % factor != 1) {
            return false;
        }

        // Both inputs satisfy the remainder condition; factor is common
        return true;
    }
}