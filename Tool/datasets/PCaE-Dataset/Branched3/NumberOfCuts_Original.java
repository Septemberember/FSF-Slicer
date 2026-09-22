public class NumberOfCuts_Original {
    // Utility: compute a simple cut count based on input n
    // This method uses a small conditional table to determine the result.

    public static int numberOfCuts(int n) {
        // Base case: if n is 1, no cuts are needed.
        if (n == 1) {
            // Base case within the first conditional
            return 0;
        }
        // If n is even, the number of cuts is n/2
        if (n % 2 == 0) {
            // Even case
            return n / 2;
        }
        // Odd n greater than 1: the number of cuts equals n
        return n;
    }
}