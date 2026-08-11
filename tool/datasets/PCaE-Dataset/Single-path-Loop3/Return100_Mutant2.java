public class Return100_Mutant2 {
    // Simple example class demonstrating a constant-returning method
    // Useful for validating iteration-based counters in isolation
    // No external dependencies; self-contained demonstration
    public static int return100 () {
        int res = 0;
        int i = 0;
        // Iterate 101 times due to inclusive bound
        for(i = 0; i <= 100; i++) { // CHANGED: condition changed to <=
            res = res + 1;
        }
        // The final result equals the number of iterations performed
        return res;
    }
}