public class NumberOfCuts_Mutant1 {

    // Utility: compute a simple cut count based on parity
    // The implementation is kept minimal and clear.

    public static int numberOfCuts(int n) {
        // Base case: when n equals 1, return 1 as specified
        if (n == 1) {
            return 1; // mutated line
        }

        // Even n yields the half-count; this is the core logic
        if (n % 2 == 0) {
            return n / 2;
        }

        // Odd n (greater than 1) leaves the count unchanged
        return n;
        // End of parity-based logic
    }

    // End of NumberOfCuts helper
}