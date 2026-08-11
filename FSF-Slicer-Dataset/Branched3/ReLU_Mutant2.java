public class ReLU_Mutant2 {

    // Mutant variant of ReLU function: non-negative inputs are passed through.
    // This demonstrates a simple conditional structure for clarity.
    public static double computeReLU(double x) {
        // Check if the input is non-negative
        if(x >= 0.0) {
            // Return the original value for non-negative inputs
            return x;
        }

        // For negative inputs, return the constant mutant value
        return 1.0;
    }
}