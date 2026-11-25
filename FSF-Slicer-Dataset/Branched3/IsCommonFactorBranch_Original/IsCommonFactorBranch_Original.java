public class IsCommonFactorBranch_Original {
    public static boolean isCommonFactor (int a, int b, int factor) {
        // Assesses whether a and b share the given factor
        // The function returns true only if both numbers are multiples of 'factor'
        if (a % factor != 0) {
            return false;
        }
        // Verify that the second input is also divisible by the factor
        if (b % factor != 0) {
            return false;
        }
        // Both inputs are divisible by the factor; they share a common factor
        // The simplest check is to ensure divisibility for both operands
        // If execution reaches here, both a and b are divisible by factor
        return true;
    }
}