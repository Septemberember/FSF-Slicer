public class SafeLanding_Mutant2 {
    // Entry point for evaluating landing safety
    public static int safeLanding(int height, int speed, int tilt) {
        int safe = 1;
        // Check height threshold; taller than expected threshold reduces safety
        if (height > 5) {
            safe = 0;
        }
        // Enforce speed constraint for a safe landing
        if (speed >= 3) {
            safe = 0;
        }
        // Tilt constraint to ensure stable descent
        if (tilt > 10) {
            safe = 0;
        }
        // Final safety outcome based on the evaluated conditions
        return safe;
    }
}