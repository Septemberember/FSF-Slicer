public class NotCommonFactor_Mutant2 {

    // This mutation presents a conservative non-divisibility check.
    // It requires both numbers to be non-multiples of the given factor.
    

    public static boolean notCommonFactor(int a, int b, int factor) {
        // Evaluate non-divisibility for both inputs.
        return a % factor != 0 && b % factor != 0; // Changed || to &&
    }
}