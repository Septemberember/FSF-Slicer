public class IsCommonFactorBranch_Mutant5 {
    // Utility: determine if a and b share a common factor exactly equal to factor.
    // The following method checks divisibility by the given factor.
    public static boolean isCommonFactor (int a, int b, int factor) {
        // Evaluate whether both inputs are divisible by the provided factor.
        if (a % factor != 0 || b % factor != 0) {
            // If either value is not divisible by the factor, the common factor condition fails.
            return false;
        }
        // When both are divisible by factor, the method will return true if reached.
        return true;
    }
    // End of evaluation block for IsCommonFactorBranch_Mutant5
}