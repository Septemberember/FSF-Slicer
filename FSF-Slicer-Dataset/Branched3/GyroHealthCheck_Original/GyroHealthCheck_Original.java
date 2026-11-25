public class GyroHealthCheck_Original {
    // GyroHealthCheck: compare axis differences and flag high variation
    public static int gyroHealthCheck(int x, int y, int z) {
        int diffXY = x - y;
        // Absolute difference for X and Y
        if (diffXY < 0) diffXY = -diffXY;
        int diffYZ = y - z;
        // Absolute difference for Y and Z
        if (diffYZ < 0) diffYZ = -diffYZ;
        int diffXZ = x - z;
        // Absolute difference for X and Z
        if (diffXZ < 0) diffXZ = -diffXZ;
        int alarm = 0;
        // Trigger alarm if any pairwise difference exceeds threshold
        if (diffXY > 10 || diffYZ > 10 || diffXZ > 10) {
            alarm = 1;
        }
        return alarm;
        // End of gyroHealthCheck calculations
    }
    // End of GyroHealthCheck_Original class
}