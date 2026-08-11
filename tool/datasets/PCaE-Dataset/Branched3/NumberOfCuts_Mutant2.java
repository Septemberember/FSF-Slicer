public class NumberOfCuts_Mutant2 {

    // Parity-based decision for number of cuts
    // Integer division by 2 for odd n is used, with n == 1 as base case.
    // Even n defaults to returning n.

    public static int numberOfCuts(int n) {
        // Start of method: compute result based on n
        if (n == 1) {
            // n equals 1: base case - no cuts
            return 0;
        }
        // Determine parity impact on the result
        if (n % 2 == 1) { // mutated line
            // Odd n: halve the value
            return n / 2;
        }
        // Even n: default to returning n
        return n;
    }
}