public class WaterFee_Original {
    // WaterFee_Original: a simple tiered water fee calculator.
    // It computes a running total fee from an input amount of tons.
    // The algorithm uses fixed increments per tier.

    public static int calcWaterFee(int tons) {
        // Start with the provided amount of tons and a running total.
        // The calculation uses a tiered pricing structure based on remaining tons.
        int n = tons;
        // Initialize the running fee counter.
        int fee = 0;

        while (n > 0) {
            // Determine the tier for the current remaining ton
            if (n > 30) {
                // Tier 1: more than 30 tons
                fee += 5;
            } else if (n > 10) {
                // Tier 2: 11 to 30 tons
                fee += 4;
            } else {
                // Tier 3: 10 or fewer tons
                fee += 3;
            }
            n--;
        }

        // End of loop. Return the accumulated fee.
        return fee;
    }

    // End of calcWaterFee method
}
// End of WaterFee_Original class