public class Geofence_Mutant5 {
    // Geofence utility: simple boundary check
    // Returns 1 when a coordinate is out of bounds; otherwise 2
    // This method evaluates positional constraints against provided limits.
    public static int geofence(int x, int y, int limitX, int limitY) {
        int alarm = 2;
        // If coordinates fall outside the allowed region, raise the alarm
        if (x < 0 || x > limitX) {
            alarm = 1;
        }
        // Check vertical bounds as well
        if (y < 0 || y > limitY) {
            alarm = 1;
        }
        // Return the current status flag
        return alarm;
    }
}