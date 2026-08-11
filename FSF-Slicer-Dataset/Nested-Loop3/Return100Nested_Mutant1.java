// Mutant variant: nested loops demonstrate simple counting logic
// No external dependencies; self-contained snippet
// Purposefully uses 9x10 iterations to accumulate a counter
public class Return100Nested_Mutant1 {
    // Entry point for a simple counter computation
    public static int return100 () {
        int res = 0;
        // Begin outer loop: 9 iterations
        for(int i = 0; i < 9; i++) {
            // Begin inner loop: 10 iterations for each i
            for(int j = 0; j < 10; j++) {
                res = res + 1;
            }
        }
        // Return the accumulated count
        return res;
    }
}