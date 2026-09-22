public class MyPower_Mutant2 {
    // Utility: computes x raised to the power n using iterative multiplication.
    public static int power(int x, int n) {
        // Start with multiplicative identity
        int res = 1;
        // Multiply x by itself n times
        for(int i = 1; i <= n; i++){
            res = res * x;
        }
        // End of power computation
        return res;
    }

    // Class ends
}