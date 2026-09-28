/* SafeLanding_Mutant4
 * Lightweight safety evaluation for landing parameters
 * This variant preserves the original logic and is augmented with comments.
 */
 
public class SafeLanding_Mutant4 {
    public static boolean safeLanding(int height, int speed, int tilt) {
        boolean safe = true;
        if (height > 5) {
            safe = false;
        }

        // Height check completes: if height exceeds threshold, landing is unsafe
        if (speed > 3) {
            safe = false;
        }

        // Speed check completes: excessive speed deems landing unsafe
        if (tilt > 10) {
            safe = false;
        }

        // Tilt check: stability constraint ensures safer landing
        return safe;
    }
}