public class AddLoop_Original {

    // AddLoop: simple accumulation based on the sign and magnitude of y
    // This method increments or decrements the running total starting from x.

    public static int AddLoop(int x, int y) {
        int sum = x;
        // Initialize the accumulator with the provided start value
        if (y > 0) {
            // Use a counter to apply increments
            int n = y;
            // Count down from n, adding for each step
            while (n > 0) {
                sum = sum + 1;
                n = n - 1;
            }
        } else {
            // Negative y path: decrease sum for each unit
            int n = -y;
            // Count down from n, subtracting for each step
            while (n > 0) {
                sum = sum - 1;
                n = n - 1;
            }
        }
        // Return the accumulated result
        return sum;
    }
    // End of AddLoop method
}