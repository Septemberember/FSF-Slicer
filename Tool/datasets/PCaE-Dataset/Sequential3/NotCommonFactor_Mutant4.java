// This file provides a simple predicate utility used in mutation analysis.
// It intentionally preserves existing logic while exposing the structure for testing.

public class NotCommonFactor_Mutant4 {

    // Public predicate: checks divisibility relations against a factor.
    // Returns true when a is not divisible by factor, or b is not congruent to 1 modulo factor.
    public static boolean notCommonFactor(int a, int b, int factor) {
        return a % factor != 0 || b % factor != 1; // Changed 0 to 1 in second condition
    }
}