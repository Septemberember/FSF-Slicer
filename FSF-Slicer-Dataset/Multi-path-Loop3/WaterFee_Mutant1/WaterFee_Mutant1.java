public class WaterFee_Mutant1 {
 // WaterFee_Mutant1: computes a tiered water service fee based on usage in tons
 // Base concept: start with a fixed base fee and add charges per usage interval
 // The calculation uses a simple loop over the input amount
    public static int calcWaterFee(int tons) {
        // Local copy of the input tons for iteration
        int n = tons;
        // Initial base fee
        int fee = 15;
        // Iterate while there is remaining usage to account for
        while (n > 0) {
            // Tier 1: very high usage
            if (n > 30) {
                fee += 5;
            } else if (n > 10) {
                // Tier 2: moderate usage
                fee += 4;
            } else {
                // Tier 3: low usage
                fee += 3;
            }
            // Consume one ton per loop iteration
            n--;
        }
        // Return the computed total fee
        return fee;
    }
}