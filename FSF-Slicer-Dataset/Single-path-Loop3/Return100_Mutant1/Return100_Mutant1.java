public class Return100_Mutant1 {
    // This class returns 200 by summing 2 in each of 100 iterations.
    // It uses a simple loop to accumulate the result.

    public static int return100 () {
        // Loop executes 100 times.
        // Each iteration adds 2 to the result.

        int res = 0;
        int i = 0;
        for(i = 0; i < 100; i++) {
            res = res + 2; // CHANGED: incremented by 2 instead of 1
        }
        // End of loop processing
        return res;
    }
    // End of return100 method
}