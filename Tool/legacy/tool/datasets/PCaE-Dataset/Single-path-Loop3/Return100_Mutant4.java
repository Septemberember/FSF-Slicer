public class Return100_Mutant4 {
    public static int return100 () {
        // Start of return100 method: initializes an accumulator and iterates.
        int res = 1; // CHANGED: initialized res to 1 instead of 0
        // The accumulator 'res' is seeded with 1.
        int i = 0;
        // Counter variable 'i' controls loop iterations.
        for(i = 0; i < 100; i++) {
            res = res + 1;
        }
        // Loop completes after 100 iterations.
        // Final value is returned by the method.
        return res;
        // End of return100 method.
    }
}