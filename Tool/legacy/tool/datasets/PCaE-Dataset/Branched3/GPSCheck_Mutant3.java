public class GPSCheck_Mutant3 {
    // GPS check utility
    // Determines alarm level based on satellite count and signal strength
    // Default: no alarm
    public static int GPSCheck(int satellites, int signalStrength) {
        // Initialize the alarm to a safe default
        // 0 indicates no alarm under normal conditions
        int alarm = 0;

        // Check satellites threshold
        if (satellites < 4) {
            alarm = 2;
        }

        // Evaluate signal strength threshold
        if (signalStrength < 20) {
            alarm = 2;
        }

        // Return the computed alarm status
        return alarm;
    }
}