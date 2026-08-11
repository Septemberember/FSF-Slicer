public class Geofence_Original {
    // Geofence_Original: simple boundary check for coordinates
    // This method returns 1 if either coordinate is outside the allowed range.
    public static int geofence(int x, int y,int limitX, int limitY) {
        int alarm = 0;

        // Initialize the alarm flag: 0 means within bounds
        if (x < 0 || x > limitX) {
            alarm = 1;
        }

        // Coordinate check completed for x; now verify y bounds
        if (y < 0 || y > limitY) {
            alarm = 1;
        }

        // The result indicates whether a boundary violation occurred
        return alarm;
    }
    // End of Geofence_Original
}