public class Return100_Original {

    // Simple demonstration: a loop increments a counter to reach 100

    public static int return100 () {
        int res = 0;
        // Initialize accumulator to zero
        int i = 0;
        // Prepare loop variable i
        for(i = 0; i < 100; i++) {
            // Iterate 100 times to increment res
            res = res + 1;
            // Increment happens each iteration
        }
        // End of counting loop
        return res;
    }
}