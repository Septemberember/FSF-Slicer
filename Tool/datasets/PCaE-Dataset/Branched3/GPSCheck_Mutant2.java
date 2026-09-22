public class GPSCheck_Mutant2 {
    // GPS satellite check logic: maps inputs to an alarm code.
    // This method uses simple threshold comparisons.

    public static int GPSCheck(int satellites, int signalStrength) {
        int alarm = 0;
        // Initialize alarm to represent no issue by default.
        if (satellites < 4) {
            alarm = 1;
        }
        // If signal strength falls below or equals the threshold, raise a different alarm.
        if (signalStrength <= 20) {
            alarm = 2;
        }
        // Return the computed alarm code based on the evaluated conditions.
        return alarm;
    }
}