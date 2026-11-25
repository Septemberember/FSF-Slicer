public class IsCommonMultiple_Mutant1 {

    // Utility note: isCommonMultiple evaluates a divisibility-based condition for m.
    // It currently returns true when m is not divisible by either a or b.
    public static boolean isCommonMultiple(int a, int b, int m) {
        // Non-divisibility by both inputs is checked below.
        return m % a != 0 && m % b != 0;
    }
}