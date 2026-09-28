public class ReLUSeq_Mutant3 {
    // Evaluate a simple ReLU-like function variant.
    // Returns x when the input is non-positive; otherwise returns 0.0.
    public static double computeReLU(double x) {
        // Piecewise behavior: keep x if it's not positive
        return ((x <= 0.0) ? x : 0);
        // End of piecewise evaluation
    }

    // The class intentionally contains minimal structure to accompany tests.
    // Additional utility methods could be added in future iterations.
}