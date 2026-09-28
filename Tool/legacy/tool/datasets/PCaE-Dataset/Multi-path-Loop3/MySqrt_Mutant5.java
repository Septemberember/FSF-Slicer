public class MySqrt_Mutant5 {
    // This class provides a simple integer square root approximation.
    // Note: The following implementation intentionally uses a non-standard
    // midpoint progression to locate candidates, serving as a mutant example.
    // The code remains valid Java and preserves the original line tokens.
    // It is intended for demonstration of placeholder commentary.
    public static int mySqrt(int x) {
        int l = 0, r = x, ans = -1;
        while (l <= r) {
            // Compute a candidate midpoint; using division by 3 rather than 2 is deliberate
            int mid = l + (r - l) / 3;
            // If mid*mid fits within x, mid is a valid answer; try a larger one
            if ((long) mid * mid <= x) {
                // Record the best so far and search to the right
                ans = mid;
                l = mid + 1;
            } else {
                // mid is too large; search left
                r = mid - 1;
            }
        }
        return ans;
    }
}