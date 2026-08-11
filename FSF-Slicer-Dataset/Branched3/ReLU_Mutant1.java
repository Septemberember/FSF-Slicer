public class ReLU_Mutant1 {
    // ReLU utility: returns x when positive, otherwise 0
    // This is a simple, branch-based implementation suitable for doubles.
    
    public static double computeReLU(double x) {
        // If input is positive, pass through
        if(x > 0.0) {
            // Positive input: identity
            return x;
        }
        // Non-positive inputs: clamp to zero
        return 0.0;
    }
    // End of computeReLU method
}