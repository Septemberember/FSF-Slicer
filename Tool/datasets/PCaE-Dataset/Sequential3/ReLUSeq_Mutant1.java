public class ReLUSeq_Mutant1 {
    // ReLU activation utility for a single scalar input.
    // This method returns the input when positive; otherwise it returns zero.
    public static double computeReLU(double x) {
        return ((x > 0.0) ? x : 0);
    }
    // Note: The implementation uses a ternary operator for clarity.
    // A minimalistic logic path could be used, but readability is preserved here.
    // This class provides a simple ReLU computation with a single method.
}