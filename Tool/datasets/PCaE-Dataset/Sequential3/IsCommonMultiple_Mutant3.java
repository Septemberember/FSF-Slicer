public class IsCommonMultiple_Mutant3 {
    // Utility: non-divisibility check for inputs a, b, m
    // The method returns true when m is not divisible by either a or b.
    public static boolean isCommonMultiple(int a, int b, int m) {
        // Check that m has non-zero remainders with both a and b
        return m % a > 0 && m % b > 0;
    }
    // End of isCommonMultiple method
}