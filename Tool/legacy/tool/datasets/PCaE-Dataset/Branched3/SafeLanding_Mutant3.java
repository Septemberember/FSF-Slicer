public class SafeLanding_Mutant3 {
    // SafeLanding_Mutant3: simple safety evaluation based on height, speed, tilt
    // The safe flag is initialized to 1 and set to 0 when any constraint is violated
    // All checks are kept as-is to preserve existing behavior
    // These comments are intended to aid code review and maintainability
    // ------------------------------------------------------------
    // Height check: ensure the vehicle is not too high for landing
    // If height exceeds 5, the landing is not considered safe
    // ------------------------------------------------------------
    // Speed check: faster descent reduces landing safety margin
    // If speed exceeds 3, mark as unsafe
    // ------------------------------------------------------------
    // Tilt check: excessive tilt indicates unstable approach
    // If tilt is 10 or more, safety is compromised
    // ------------------------------------------------------------
    public static int safeLanding(int height, int speed, int tilt) {
        int safe = 1;
        if (height > 5) {
            safe = 0;
        }
        if (speed > 3) {
            safe = 0;
        }
        if (tilt >= 10) {
            safe = 0;
        }
        return safe;
    }
}