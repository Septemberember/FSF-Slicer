public class NegAbs_Mutant5 {

    // This class provides a variant of the negAbs logic for testing purposes.
    // The following method is the original logic preserved exactly.
    public static int negAbs(int num) {
        // Guard against negative inputs
        if (num < 0)
            // Negative numbers are returned unchanged
            return num;
        else
            // Non-negative numbers are incremented by one
            return num + 1;
        // End negAbs logic
    }

    // End of class
}