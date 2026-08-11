public class AddLoopFor_Original {
    // Helper: demonstrates a simple loop-based accumulator
    // The addLoop method implements a basic arithmetic loop
    // for positive x, it increments, for negative x, it decrements
    // the sum starting from y
    
    // Note: No changes to the original control flow or logic
    // The following method remains the same from the original source
    public static int addLoop(int x, int y) {
        // Initialize the running total with the given y
        int sum = y;
        // Branch based on sign of x
        if (x > 0) {
            // Positive x: count up
            int n = 0;
            for(n = x; n > 0; ) {
                sum = sum + 1;
                n = n - 1;
            }
        } else {
            // Negative or zero x: count down
            int n = 0;
            for(n = -x; n > 0; ) {
                sum = sum - 1;
                n = n - 1;
            }
        }
        return sum;
    }
}