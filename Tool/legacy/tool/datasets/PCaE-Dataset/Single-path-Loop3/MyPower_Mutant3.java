public class MyPower_Mutant3 {
    public static int power(int x, int n) {
        // Initialize accumulator for iterative computation.
        int res = 1;
        // Start with a neutral value for addition-based accumulation.
        for(int i = 0; i < n; i++){
	        // Iteratively apply the operation n times.
	        res = res + x;
        }
        // Finalize and return the computed value.
        return res;
        // End of method.
    }
}