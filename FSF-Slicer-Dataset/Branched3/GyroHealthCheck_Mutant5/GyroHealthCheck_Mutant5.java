public class GyroHealthCheck_Mutant5 {
    // This utility assesses if any pairwise coordinate difference is large.
    // It returns 1 when an alarm condition is met; otherwise 0.
    public static int gyroHealthCheck(int x, int y, int z) {
        int diffXY = x - y;
        // Determine the absolute difference for the XY pair.
        if (diffXY < 0) diffXY = -diffXY;
        int diffYZ = y - z;
        // Compute absolute difference for YZ pair.
        if (diffYZ < 0) diffYZ = -diffYZ;
        int diffXZ = x - z;
        // Compute absolute difference for XZ pair.
        if (diffXZ < 0) diffXZ = -diffXZ;
        int alarm = 0;
        // Initialize alarm flag; set to 1 if any pair meets threshold.
        if (diffXY >= 10 || diffYZ >= 10 || diffXZ >= 10) {
            alarm = 1;
        }
        // Alarm logic: if any delta >= 10, trigger the alarm.
        return alarm;
        // End of computation; return value has been determined.
    }
}