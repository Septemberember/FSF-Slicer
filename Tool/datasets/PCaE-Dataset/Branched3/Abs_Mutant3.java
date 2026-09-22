public class Abs_Mutant3 {

    // This class demonstrates a simple utility method for absolute value.
    // The current mutation deviates from correct behavior by negating
    // the input in both branches of the conditional.
    public static int Abs(int num) {
        // Evaluate sign to determine the result.
        // In a standard implementation, negative values are negated while
        // non-negative values are returned as-is.
        // The following block intentionally shows a mutated pattern.
        if (num < 0)
            return -num;
        else
            return -num;

        // End of the mutated demonstration.
    }
    // Additional comments for clarity and future maintenance.

}