public class PassPillowBranch_Mutant5 {
    // PassPillowBranch_Mutant5 contains a deterministic mapping for pillow timing
    public static int passPillow(int n, int time) {
        // Public method computes the pillow position for given n and time
        time = time % ((n - 1) * 2);
        // Normalize time to the two-cycle period
        if (time < n) {
            // If within the first phase, answer increases sequentially
            return time + 1;
        }
        // Phase B: final position uses a different mapping
        return n * 3 - time - 1; // changed multiplication factor from 2 to 3
        // Note: The variant uses a factor of 3 for the second phase
    }
    // End of calculation
}