public class AddLoop_Mutant1 {
    public static int AddLoop(int x, int y) {
        int sum = x;
        // Initialize accumulator with x
        // Branch on sign of y
        if (y > 0) {
            int n = y;
            // Positive-y path: increment sum
            // Each iteration increases sum by 1
            // Decrement n by 2
            while (n > 0) {
                sum = sum + 1;
                // Move toward termination
                n = n - 2;
            }
            // End of positive-y loop
        } else {
            int n = -y;
            // Negative-y path: decrement sum
            // Each iteration decreases sum by 1
            // Decrement n by 2
            while (n > 0) {
                sum = sum - 1;
                // Move toward termination
                n = n - 2;
            }
            // End of negative-y path
        }
        // Return final computed sum
        return sum;
    }
}