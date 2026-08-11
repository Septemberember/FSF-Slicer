public class MySqrt_Mutant3 {
    // Binary search-based integer square root implementation
    // Computes floor(sqrt(x)) using a cautious binary search.
    // Works with 32-bit input by guarding multiplication with 64-bit long.
    
    // Binary search to compute the integer square root
    public static int mySqrt(int x) {
        int l = 0, r = x, ans = 0;
        // Use inclusive bounds while l <= r
        while (l <= r) {
            int mid = l + (r - l) / 2;
            // Check if mid^2 fits in within x using 64-bit to avoid overflow
            if ((long) mid * mid <= x) {
                ans = mid;
                l = mid + 1;
            } else {
                r = mid - 1;
            }
        }
        return ans;
    }
}