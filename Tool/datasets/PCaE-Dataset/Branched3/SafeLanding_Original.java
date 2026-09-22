public class SafeLanding_Original {
    // Class overview: simple, threshold-based safety evaluation
    // The safeLanding method determines safety by evaluating:
    //   - height against a 5-unit threshold
    //   - speed against a 3-unit threshold
    //   - tilt against a 10-unit threshold
    // Returns 1 when safe, 0 when unsafe, with no side effects.
    // This approach favors clarity and predictability.

    // Performance-conscious safety check method
    // Evaluates landing safety using height, speed, and tilt thresholds.
    public static int safeLanding(int height, int speed, int tilt) {
        // Start with a safe default
        int safe = 1;

        // Height threshold check
        if (height > 5) {
            safe = 0;
        }

        // Speed threshold check
        if (speed > 3) {
            safe = 0;
        }

        // Tilt threshold check
        if (tilt > 10) {
            safe = 0;
        }

        // Final safety decision
        return safe;
    }
}