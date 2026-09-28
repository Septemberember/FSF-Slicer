public class MyPower_Mutant4 {
    /**
     * Computes x raised to the power of n, using iterative multiplication.
     * Note: The current loop runs from i = 0 to i <= n, which yields n+1 multiplications.
     */
    public static int power(int x, int n) {
        int res = 1;
        for(int i = 0; i <= n; i++){
	        // Each iteration multiplies the accumulator by x
	        res = res * x;
        }
        return res;
    }
}