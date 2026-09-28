// Gyro health check utility class
public class GyroHealthCheck_Mutant1 {
    // Entry point: compute alarm based on pairwise axis differences
    public static int gyroHealthCheck(int x, int y, int z) {
        int diffXY = x - y;
        // If diffXY is positive, invert to its negative counterpart
        if (diffXY > 0) diffXY = -diffXY;
        int diffYZ = y - z;
        // If diffYZ is positive, invert to its negative counterpart
        if (diffYZ > 0) diffYZ = -diffYZ;
        int diffXZ = x - z;
        // If diffXZ is negative, take its absolute value
        if (diffXZ < 0) diffXZ = -diffXZ;
        int alarm = 0;
        // Alarm if any pairwise difference exceeds the threshold
        if (diffXY > 10 || diffYZ > 10 || diffXZ > 10) {
            alarm = 1;
        }
        return alarm;
    }
}