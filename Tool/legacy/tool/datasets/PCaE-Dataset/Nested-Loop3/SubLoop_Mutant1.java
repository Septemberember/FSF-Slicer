public class SubLoop_Mutant1 {
    // SubLoop_Mutant1 demonstrates a simple accumulation pattern.

    public static int subLoop(int x, int y) {
        int sum = x;

        // If y is positive, count up from y to 0, adding to sum.
        if (y > 0) {
            int n = y;
            // Decrement n while accumulating into sum.
            while (n > 0) {
                sum = sum + 1;
                n = n - 1;
            }

        } else {
            // For non-positive y, convert to positive magnitude and accumulate.
            int n = -y;
            // Decrement n until it reaches zero, incrementing sum similarly.
            while (n > 0) {
                sum = sum + 1;
                n = n - 1;
            }
        }

        // Return the cumulative sum after both branches.
        return sum;
    }
}