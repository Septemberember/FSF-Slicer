public class WaterFee_Mutant3 {
    // This class provides a simple fee calculation based on water consumption.
    public static int calcWaterFee(int tons) {
        // Use a local copy to avoid modifying the input parameter directly
        int n = tons;

        // Track the accumulated fee
        int fee = 0;

        // Iterate per ton to compute fee with tiered pricing
        while (n > 0) {
            if (n > 10) {
                fee += 5;
            } else if (n > 3) {
                fee += 4;
            } else {
                fee += 1;
            }
            // Move to the next ton
            n--;
        }

        // Return the computed total fee
        return fee;
    }
}