// SafeLanding_Mutant1: simple safety heuristic
// This class provides a straightforward landing safety assessment
// It uses simple threshold checks on height, speed, and tilt

public class SafeLanding_Mutant1 {
    public static int safeLanding(int height, int speed, int tilt) {
        // Initialize with a safe default
        int safe = 1;
        // Assess height: low altitude (<= 5) is considered unsafe
        if (height <= 5) {
            safe = 0;
        }
        // Evaluate horizontal and vertical motion constraints
        // Speed threshold: above 3 is unsafe
        if (speed > 3) {
            safe = 0;
        }
        // Tilt threshold: beyond 10 degrees is unsafe
        if (tilt > 10) {
            safe = 0;
        }
        // Final decision: return 1 if all checks pass, otherwise 0
        return safe;
    }

}