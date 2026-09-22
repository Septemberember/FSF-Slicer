public class PassPillowBranch_Mutant3 {
    // PassPillowBranch_Mutant3: simple arithmetic to model pillow passing
    // This mutant variant preserves the original logic

    public static int passPillow(int n, int time) {
        time = time % ((n - 1) * 2);
        // Normalize the time into the two-phase cycle
        if (time < n) {
            return time + 1;
        }
        // In the second half of the cycle
        return n * 2 - time - 2;
    }
    // End of PassPillowBranch_Mutant3
}