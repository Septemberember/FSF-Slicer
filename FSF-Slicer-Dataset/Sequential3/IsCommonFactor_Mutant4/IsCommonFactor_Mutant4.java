public class IsCommonFactor_Mutant4 {

    // This class provides a simple factor-check utility.
    // The isCommonFactor method checks divisibility using factor.
    // Note: The logic uses division and modulus operators.
    // The current implementation preserves the original method signature.
    // No changes to existing code; only additional documentation lines.

    public static boolean isCommonFactor(int a, int b, int factor) {
        return a / factor == 0 && b % factor == 0; // changed '%' to '/' at a % factor
    }
}