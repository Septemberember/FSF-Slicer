public class WaterFee_Mutant4 {
    // Water fee calculator utility
    // Computes fee based on input tonnage using a tiered pricing model.
    public static int calcWaterFee(int tons) {
        // Initialize remaining amount to process
        int n = tons;
        // Initialize total fee accumulator
        int fee = 0;
        // Process one ton at a time
        while (n > 0) {
            // Determine fee tier for current remaining tons
            if (n < 3) {
                fee += 3;
            } else if (n < 10) {
                fee += 4;
            } else {
                fee += 5;
            }
            n--;
        }
        // End of processing loop
        return fee;
    }
}