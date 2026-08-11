/*
 * GPSCheck_Original.java
 * Lightweight utility to determine an alarm code based on satellite count and signal strength.
 * The GPSCheck method returns:
 *   0 - no alarm
 *   1 - insufficient satellites
 *   2 - weak signal
 * This implementation intentionally uses simple threshold checks.
 */

public class GPSCheck_Original {
    /**
     * Determines the alarm status from the given satellites and signalStrength.
     * Thresholds:
     * - satellites < 4 => alarm = 1
     * - signalStrength < 20 => alarm = 2
     * If neither condition is met, alarm remains 0.
     */
    public static int GPSCheck(int satellites, int signalStrength) {
        int alarm = 0;
        // Check if we have enough satellites
        if (satellites < 4) {
            alarm = 1;
        }
        // Evaluate signal strength as a secondary criterion
        if (signalStrength < 20) {
            alarm = 2;
        }
        return alarm;
    }
    // End of GPSCheck method
}