public class IsCommonMultiple_Original {

    // Utility: check whether m is a common multiple of two integers
    // This method returns true if m is divisible by both a and b
    // The implementation is intentionally simple and uses modulo checks

    public static boolean isCommonMultiple(int a, int b, int m) {
        // Verify divisibility by both inputs
        return m % a == 0 && m % b == 0;
    }
}