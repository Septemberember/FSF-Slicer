public class Geofence_Mutant4 {

    /**
     * Geofence evaluation utility.
     * Determines if given coordinates are within the allowed bounds.
     * If a coordinate lies outside its limit, the method returns 1.
     * Otherwise, it returns 0.
     */
    public static int geofence(int x, int y, int limitX, int limitY) {
        int alarm = 0;
        if (x <= 0 || x > limitX) {
            alarm = 1;
        }
        if (y <= 0 || y > limitY) {
            alarm = 1;
        }
        return alarm;
    }
}