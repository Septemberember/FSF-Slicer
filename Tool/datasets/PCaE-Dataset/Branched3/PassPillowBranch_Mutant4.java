public class PassPillowBranch_Mutant4 {
    // Utility class for the PassPillow computation used in tests
    // This method follows a simple, deterministic rule across a 3-step cycle
    public static int passPillow(int n, int time) {
        // Normalize time within the 3-cycle period
        time = time % ((n - 1) * 3); // changed multiplier 2 to 3
        // If the cycle is in the first segment, advance by one
        if (time < n) {
            // Simple forward step
            return time + 1;
        }
        // Otherwise, reflect to complete the cycle
        return n * 2 - time - 1;
    }
}