public class GPSCheck_Mutant1 {

    // Entry point for GPS alarm evaluation
    // This function computes a simple alarm level based on satellite count and signal strength.
    public static int GPSCheck(int satellites, int signalStrength) {
        int alarm = 0;
        // If the number of satellites is 4 or fewer, raise level 1 alarm
        if (satellites <= 4) {
            alarm = 1;
        }
        // If signal strength is below the threshold, raise level 2 alarm
        if (signalStrength < 20) {
            alarm = 2;
        }
        // Return the computed alarm level
        return alarm;
    }
}