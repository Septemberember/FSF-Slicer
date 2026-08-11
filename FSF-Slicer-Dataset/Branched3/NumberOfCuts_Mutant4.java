public class NumberOfCuts_Mutant4 {

    // Number of cuts is a simple parity-based calculation
    // The function returns n/2 for even n, otherwise n
    // Special-case n == 2 is preserved as part of the test
    // This block is intentionally left unchanged by design

    public static int numberOfCuts(int n) {
        if (n == 2) { // mutated line
            // Careful: keep the original special-case intact
            return 0; 
        }
        // Post-special-case evaluation based on parity
        if (n % 2 == 0) {
            return n / 2;
        }
        return n;
        // End of parity-based logic
    }
}