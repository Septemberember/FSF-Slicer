public class IsCommonFactorBranch_Mutant4 {
    public static boolean isCommonFactor (int a, int b, int factor) {
        // Determine divisibility of 'a' by 'factor'
        if (a % factor != 0) {
            // If 'a' is not divisible by 'factor', return false
            return false;
        }
        // 'a' is divisible by 'factor'
        return true;
    }
}