// IsCommonFactor_Original: utility to verify if two integers share a given common factor
// This simple predicate returns true when both a and b are divisible by factor.
// No state is stored; the check is purely functional.

public class IsCommonFactor_Original {

    public static boolean isCommonFactor(int a, int b, int factor) {
        // Evaluate divisibility for both inputs
        return a % factor == 0 && b % factor == 0;
    }
}