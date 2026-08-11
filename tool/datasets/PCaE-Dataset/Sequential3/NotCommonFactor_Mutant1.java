public class NotCommonFactor_Mutant1 {
    // Utility: simple predicate for factor-related checks
    // This class is a minimal example used for mutation testing

    
    public static boolean notCommonFactor(int a, int b, int factor) {
        // Evaluate divisibility relation with the provided factor
        return a % factor == 0 || b % factor != 0; // Changed != to ==
    }
 // End of class for NotCommonFactor_Mutant1
}