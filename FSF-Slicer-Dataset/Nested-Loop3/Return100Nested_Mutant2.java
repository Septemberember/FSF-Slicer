public class Return100Nested_Mutant2 {

    // Helper: compute a value by nested counting loops.
    // The method returns the total number of increments performed.
    // Note: this mirrors a simple nested-loop counting pattern.
    public static int return100 () {
        int res = 0;
        // Outer loop runs 10 times
        for(int i = 0; i < 10; i++) {
            // Inner loop runs 9 times per outer iteration
            for(int j = 0; j < 9; j++) {
                res = res + 1;
            }
        }
        // Final accumulated result is returned
        return res;
    }
}