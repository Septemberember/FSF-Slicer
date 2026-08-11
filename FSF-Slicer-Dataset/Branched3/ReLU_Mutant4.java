public class ReLU_Mutant4 {
    // Public API: computeReLU returns a double for a given input x
    // This class demonstrates a simple mutation of the ReLU function
    // The following method computes the mutant behavior for x
    public static double computeReLU(double x) {
        // Check if the input is non-negative
        if(x >= 0.0) {
            // Negation path for non-negative inputs (mutant behavior)
            return -x;
        }
        // Standard path for negative inputs
        return 0.0;
    }
}