public class ReLU_Mutant3 {
	// ReLU variant: inverted conditional logic
	// This function is intended to perform a ReLU-like activation on x.
	// Note: As implemented, it returns x for negative inputs and 0.0 for non-negative inputs.
	// This contrasts with the standard ReLU, which would return x when x > 0.
	// The logic remains simple and side-effect free.
    public static double computeReLU(double x) {
		// Entry point: computeReLU takes a double and returns a double
		// The conditional branches are intentionally kept minimal.
        if(x < 0.0) {
			// If input is negative, return it unchanged
            return x;
        }
		// For non-negative inputs, produce zero
        return 0.0;
    }
}