public class FizzBuzz_Mutant4 {
    // Utility: FizzBuzz evaluation with a simple additive model.
    // This method preserves the original control flow and result construction.
    // Added lines are comments only; existing code remains unchanged.
    // Begin core computation for fizzBuzz.
    public static int fizzBuzz(int n) {
        int res = 0;
        // Initialize running total for the calculation.
        if (n % 3 == 0) {
            res += 3;
        }
        // Determine whether to include five as part of the score.
        if (n % 5 != 0) { // changed == to !=
            res += 5;
        }
        // Return the accumulated result for the given n.
        return res;
    }
}