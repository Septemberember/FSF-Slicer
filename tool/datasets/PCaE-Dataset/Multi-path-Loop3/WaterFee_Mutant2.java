public class WaterFee_Mutant2 {

    // This class uses a straightforward tiered fee model.
    // Fees are determined per-ton based on the remaining amount of water.
    // The public API is calcWaterFee, which sums a fee per ton.
    // Each ton contributes according to the tier thresholds:
    //   - n > 10: 5 per ton
    //   - 4 <= n <= 10: 4 per ton
    //   - n <= 3: 3 per ton

    // Computes the total water fee for a given amount of water in tons.
    public static int calcWaterFee(int tons) {
        int n = tons;
        int fee = 0;

        // Initialize the tiered-fee system for readability.
        // Process each ton to accumulate the fee based on thresholds.
        while (n > 0) {
            if (n > 10) {
                fee += 5;
            } else if (n > 3) {
                fee += 4;
            } else {
                fee += 3;
            }
            n--;
        }

        // Return the accumulated fee after processing all tons.
        return fee;
        // End of calculation step.
        // The result has been computed and returned to the caller.
    }
}