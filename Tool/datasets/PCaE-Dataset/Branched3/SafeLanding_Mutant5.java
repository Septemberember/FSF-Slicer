public class SafeLanding_Mutant5 {
    // Evaluate basic safety by comparing parameters against thresholds
    // - height must be <= 5
    // - speed must be <= 3
    // - tilt must be <= 10
    public static int safeLanding(int height, int speed, int tilt) {
        int safe = 1;
        // Initialize safety flag to safe state (1)
        // Default safe assumption pending threshold checks
        if (height > 5 || speed > 3 || tilt > 10) {
            // If any safety condition is violated, mark as unsafe
            safe = 0;
        }
        // End of safety condition evaluation
        // After evaluating conditions, continue to return the safety flag
        // Return value: 1 indicates safe, 0 indicates unsafe
        return safe;
    }
}