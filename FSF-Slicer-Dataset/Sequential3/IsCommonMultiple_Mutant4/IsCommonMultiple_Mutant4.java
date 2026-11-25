public class IsCommonMultiple_Mutant4 {
    // The IsCommonMultiple operation checks if a number m is a multiple of both a and b.
    // In typical mathematical terms, m is a common multiple of a and b when m % a == 0 and m % b == 0.
    // This mutant variant uses a nonstandard condition to exercise test coverage.
    // Note: Java's remainder operation (m % a) can be negative when m and a have opposite signs.
    // The following logic intentionally deviates from the standard check as a mutation.
    // The original, conventional form would be: (m % a == 0) && (m % b == 0)
    public static boolean isCommonMultiple(int a, int b, int m) {
        // This mutant uses a sign-based check rather than equality to zero.
        return m % a < 0 && m % b < 0;
    }
}