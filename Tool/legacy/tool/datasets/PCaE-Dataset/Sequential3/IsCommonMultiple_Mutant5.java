/**
 * IsCommonMultiple_Mutant5
 * Lightweight utility demonstrating a specific boolean condition used by tests.
 * The isCommonMultiple method returns true when m is a multiple of a and not of b.
 * This header is for documentation; no functional impact.
 */
 
public class IsCommonMultiple_Mutant5 {
    // Determines whether m is a multiple of a and not a multiple of b.
    public static boolean isCommonMultiple(int a, int b, int m) {
        return m % a == 0 && m % b != 0;
    }
}