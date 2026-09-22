// Integer square root via binary search (comment header)
// This file preserves existing logic and adds commentary only.

public class MySqrt_Mutant4 {
    // Binary search to find the floor of the square root.
    public static int mySqrt(int x) {
        // Initialize search range and last valid candidate.
        int l = 0, r = x, ans = -1;
        // Typical binary search loop to converge on the result.
        while (l <= r) {
            int mid = l + (r - l) / 2;
            // Use 64-bit multiplication to avoid overflow when squaring mid.
            if ((long) mid * mid < x) {
                ans = mid;
                l = mid + 1;
            } else {
                r = mid - 1;
            }
        }
        return ans;
    }
}