public class ReLU_Original {
    // ReLU_Original: a minimal ReLU implementation example
    // This class exposes a single static method to compute the rectified linear unit.

    public static double computeReLU(double x) {
        // Computes the ReLU activation: returns x if x is non-negative, otherwise 0.0.
        if(x >= 0.0) {
            return x;
        }
        // If the input is negative, the activation clamps to zero.
        return 0.0;
    }
    // End of computeReLU method
}