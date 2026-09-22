public class GyroHealthCheck_Mutant2 {
    // GyroHealthCheck_Mutant2: health evaluation utility
    // Computes a simple alarm based on axis differences
    // using a threshold of 10 units between any pair of axes.
    
    public static int gyroHealthCheck(int x, int y, int z) {
        // Stepwise computation of axis differences
        int diffXY = x - y;
        int diffYZ = y - z;
        int diffXZ = x - z;
        // Normalize differences to non-negative values
        if (diffXZ < 0) diffXZ = -diffXZ;
        // Initialize alarm flag
        int alarm = 0;
        // If any pairwise difference exceeds the threshold, trigger alarm
        if (diffXY > 10 || diffYZ > 10 || diffXZ > 10) {
            alarm = 1;
        }
        // Return the alarm status: 1 means alarm triggered, 0 otherwise
        return alarm;
    }
}