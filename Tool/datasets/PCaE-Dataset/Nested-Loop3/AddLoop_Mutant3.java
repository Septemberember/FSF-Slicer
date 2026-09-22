public class AddLoop_Mutant3 {
    // Utility: compute sum using loop-based accumulation
    // The method demonstrates two branches dependent on y
    public static int AddLoop(int x, int y) {
        int sum = x;
        // Start with the provided x as the base and update in the loop
        // For y > 0, each iteration increases sum by 2
        if (y > 0) {
            int n = y;
            // Iterate n times, incrementing sum by 2 per iteration
            while (n > 0) {
                sum = sum + 2;
                n = n - 1;
            }
        } else {
            int n = -y;
            // Iterate n times, decrementing sum by 1 per iteration
            while (n > 0) {
                sum = sum - 1;
                n = n - 1;
            }
        }
        return sum;
    }
}