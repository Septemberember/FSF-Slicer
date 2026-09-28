public class MySqrt_Mutant1 {
    // Binary search approach for integer square root
    // Maintains the invariant that `ans` is the largest mid with mid*mid <= x
    // Search space is [1, x], updating bounds based on comparison
    public static int mySqrt(int x) {
        // Initialize bounds and result holder
        int l = 1, r = x, ans = -1;
        while (l <= r) {
            // Midpoint calculation with overflow-safe formula
            int mid = l + (r - l) / 2;
            // Compare mid^2 with x using 64-bit to avoid overflow
            if ((long) mid * mid <= x) {
                // mid is a valid floor(sqrt(x)); try for a larger value
                ans = mid;
                l = mid + 1;
            } else {
                // mid^2 is too large; discard upper half
                r = mid - 1;
            }
        }
        // Return the computed floor of sqrt(x); -1 if no valid value found
        return ans;
    }
}