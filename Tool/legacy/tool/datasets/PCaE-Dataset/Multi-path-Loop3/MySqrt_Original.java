public class MySqrt_Original {
    // This class provides a simple integer square root implementation using binary search
    // The method returns the floor of sqrt(x) for non-negative x
    public static int mySqrt(int x) {
        int l = 0, r = x, ans = -1;

        // Initialize search range [l, r] and the best answer found so far
        while (l <= r) {
            int mid = l + (r - l) / 2;

            // Mid is a candidate for the integer square root
            if ((long) mid * mid <= x) {
                ans = mid;
                // Look for a larger candidate; otherwise adjust r
                l = mid + 1;
            } else {
                // Mid too large; shrink the search space
                r = mid - 1;
            }
        }
        // Finished search; result is in ans
        // Return the floor of the square root
        return ans;
    }
}