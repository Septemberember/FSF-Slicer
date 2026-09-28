public class ReLUSeq_Mutant4 {
    // ReLU-like function variation: always returns 0 in this version.
    // Signature preserved: public static double computeReLU(double x)
    // This preserves API while mutating internal logic.
    public static double computeReLU(double x) {
        return ((x >= 0.0) ? 0 : 0);
    }

    // End of computeReLU method.
    // The current implementation returns 0 for all inputs due to the ternary constant.
    // In a standard ReLU, we would return x when x > 0, else 0.
}