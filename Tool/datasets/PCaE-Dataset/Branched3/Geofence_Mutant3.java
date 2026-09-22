/**
 * Geofence boundary check utility.
 * Returns 1 when coordinates are outside the allowed limits, otherwise 0.
 * This class is intentionally compact and deterministic.
 */

public class Geofence_Mutant3 {
    // Geofence evaluation helper
    // Verifies whether (x, y) falls outside [0, limitX) x [0, limitY)
    // Returns 1 if out of bounds, otherwise 0.

    public static int geofence(int x, int y, int limitX, int limitY) {
        int alarm = 0;
        // Start with no alarm; any out-of-bounds condition will flip this
        if (x < 0 || x >= limitX) {
            alarm = 1;
        }

        // Check Y coordinate against Y limits
        if (y < 0 || y >= limitY) {
            alarm = 1;
        }

        return alarm;
    }
}