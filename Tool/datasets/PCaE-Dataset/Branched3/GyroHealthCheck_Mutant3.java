public class GyroHealthCheck_Mutant3 {
    // Simple health check utility based on input differences
    // This method evaluates if all pairwise differences exceed a threshold.
    public static int gyroHealthCheck(int x, int y, int z) {
        // Compute absolute differences between input values
        // diffXY = |x - y|
        // diffYZ = |y - z|
        // diffXZ = |x - z|
        int diffXY = x - y;
        if (diffXY < 0) diffXY = -diffXY;
        int diffYZ = y - z;
        if (diffYZ < 0) diffYZ = -diffYZ;
        int diffXZ = x - z;
        if (diffXZ < 0) diffXZ = -diffXZ;
        int alarm = 0;
        // If all pairwise differences exceed 10, raise alarm
        if (diffXY > 10 && diffYZ > 10 && diffXZ > 10) {
            // Alarm state activated
            alarm = 1;
        }
        // Return whether an alarm condition was met
        return alarm;
    }
    // End of gyroHealthCheck
}