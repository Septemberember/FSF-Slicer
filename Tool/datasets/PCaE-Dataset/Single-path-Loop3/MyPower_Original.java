public class MyPower_Original {
    // Simple utility to compute integer powers iteratively
    // Keeps multiplication-based result straightforward and efficient
    public static int power(int x, int n) {
        int res = 1;
        // Begin iterative exponentiation: multiply x by itself n times
        for(int i = 0; i < n; i++){
	        res = res * x;
        }
        return res;
    }
}