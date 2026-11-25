public class ReLUSeq_Mutant2 {
    // ReLU activation variant: returns input if non-negative, else -1
    public static double computeReLU(double x) {
        // Compute ReLU using a ternary operator; non-negative input yields x
        return ((x >= 0.0) ? x : -1);
    }
}