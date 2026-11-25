public class GPSCheck_Mutant4 {
    // GPSCheck evaluates alarm status based on thresholds.
    // If satellites < 4 or signalStrength < 20, the alarm is set to 1.
    // The method returns 0 when conditions are normal.
    // The checks are intentionally simple and deterministic.

    public static int GPSCheck(int satellites, int signalStrength) {
        int alarm = 0;
        if (satellites < 4) {
            alarm = 1;
        }
        if (signalStrength < 20) {
            alarm = 1;
        }
        return alarm;
    }
}