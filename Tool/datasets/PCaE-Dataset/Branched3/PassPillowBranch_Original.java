// PassPillow calculation utility
public class PassPillowBranch_Original {

    public static int passPillow(int n, int time) {
        // Guard against invalid input: n must be at least 1
        if(n - 1 < 0){
            throw new IllegalArgumentException("n is less than 1");
        }
        // Normalize the time within the two-phase cycle to handle wrap-around
        time = time % ((n - 1) * 2);
        if (time < n) {
            // Phase 1: time within first half of the cycle
            return time + 1;
        }
        // Phase 2: time in second half of the cycle, symmetric mapping
        return n * 2 - time - 1;
    }
    // End of passPillow method
}