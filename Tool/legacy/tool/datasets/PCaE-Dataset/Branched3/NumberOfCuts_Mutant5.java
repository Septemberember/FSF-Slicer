public class NumberOfCuts_Mutant5 {

    // Overview of the algorithm
    // This method returns the number of cuts for a given n using a parity-based rule.
    // - If n == 1, the result is 0.
    // - If n is even, the result is n - 1.
    // - If n is odd (and not 1), the result is n.
    public static int numberOfCuts(int n) {
        if (n == 1) {
            return 0;
        }
        if (n % 2 == 0) {
            return n - 1; // mutated line
        }
        return n;
    }
}