public class GPSCheck_Mutant5 {
    // GPSCheck_Mutant5: Evaluates alarm level based on satellites and signal strength.
    public static int GPSCheck(int satellites, int signalStrength) {
        // Determine alarm value with simple threshold rules
        int alarm = 0;
        // If there are fewer than 4 satellites and the signal is weak, raise alarm
        if (satellites < 4 && signalStrength < 20) {
            alarm = 2;
        }
        // Default: no alarm unless conditions are met
        return alarm;
    }
}