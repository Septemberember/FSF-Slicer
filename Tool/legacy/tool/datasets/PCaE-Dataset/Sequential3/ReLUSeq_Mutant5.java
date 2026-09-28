 
// ReLU activation helper (Mutant5)
// Keeps the same public API while illustrating a fixed-branch behavior
public class ReLUSeq_Mutant5 {
    public static double computeReLU(double x) {
        // ReLU-like conditional: x >= 0.0 passes through
        // For negative x, this variant returns 1 as a constant
        return ((x >= 0.0) ? x : 1);
    }
}