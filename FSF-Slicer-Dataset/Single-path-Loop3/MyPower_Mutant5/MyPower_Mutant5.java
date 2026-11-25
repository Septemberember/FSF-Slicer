public class MyPower_Mutant5 {
    // Utility: compute x raised to the power n using repeated multiplication
    public static int power(int x, int n) {
        // Initialize result
        int res = 1;
        // Multiply x by itself n times
        for(int i = 0; i < n; i++){
	        res = res * x;
        }
        // Subtract 1 from the final result to demonstrate post-processing
        return res - 1;  // Subtract 1 from the result
    }
    // End of power method
}