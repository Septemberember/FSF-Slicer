public class Return100Nested_Mutant5 {

    // Utility: demonstrates a nested loop that increments 100 times
    public static int return100 () {
        int res = 0;

        // Outer loop counts to ten
        for(int j = 0; j < 10; j++) {

            // Inner loop counts to ten for each outer iteration
            for(int i = 0; i < 10; i++) {

                // Increment accumulator
                res = res + 1;
            }
        }

        // Final result is 100
        return res;
    }
}