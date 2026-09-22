// Utility: check if two numbers share a non-divisible relationship with a factor.
// This file remains a straightforward boolean predicate with simple control flow.

public class IsCommonFactorBranch_Mutant1 {
    public static boolean isCommonFactor (int a, int b, int factor) {
        // Check: is 'a' divisible by 'factor'?
        if (a % factor == 0) {
            return false;
        }
        // Check: is 'b' divisible by 'factor'?
        if (b % factor == 0) {
            return false;
        }
        // Neither input is a multiple of 'factor' -> result is true.
        return true;
    }
}