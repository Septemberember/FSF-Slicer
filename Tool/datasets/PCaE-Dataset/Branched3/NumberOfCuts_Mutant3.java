public class NumberOfCuts_Mutant3 {

    // Helper: computes number of cuts for given n
    public static int numberOfCuts(int n) {
        // Base case: when only one piece remains, no cuts are needed
        if (n == 1) {
            return 0;
        }

        // If n is odd, with a single cut strategy this path returns n/2
        // Note: this branch mirrors a common parity-based optimization
        // The original mutation point is located on the condition below
        if (n % 2 != 0) { // mutated line
            return n / 2; 
        }

        // For even n, the default behavior is to return n
        return n;
    }

    // End of numberOfCuts()
}