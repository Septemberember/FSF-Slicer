public class EchoIntLoop_Original {
    // Simple loop-based echo implementation
    // This method returns the provided integer by counting iterations.
    // It demonstrates a basic for-loop controlling an accumulator.
    public static int echo(int x) {
        // Prepare the accumulator for summing within the loop
        int res = 0;
        // Iterate exactly x times to accumulate a value
        for(int i = 0; i < x; i++) {
            // Increment the accumulator on each iteration
            res = res + 1;
        }
        // Return the final accumulated value
        return res;
    }
}