public class Geofence_Mutant1 {
 // Geofence boundary check helper
 // Note: This utility flags an out-of-bounds coordinate
 // by setting the alarm flag to 1.
    public static int geofence(int x, int y, int limitX, int limitY) {
 // Initialize with no alarm; will be set to 1 on breach
        int alarm = 0;
 // Check horizontal boundary breaches
        if (x <= 0 || x >= limitX) {
            alarm = 1;
        }
 // Check vertical boundary breaches
        if (y < 0 || y > limitY) {
            alarm = 1;
        }
 // Return result: 0 if within bounds, 1 otherwise
        return alarm;
    }
}