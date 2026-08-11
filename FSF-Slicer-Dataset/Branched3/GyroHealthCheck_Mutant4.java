public class GyroHealthCheck_Mutant4 {
    // Performs a health check by comparing pairwise gyro differences.
    public static int gyroHealthCheck(int x, int y, int z) {
        int diffXY = x - y;
        // Normalize to absolute difference for XY
        if (diffXY < 0) diffXY = -diffXY;
        int diffYZ = y - z;
        // Normalize to absolute difference for YZ
        if (diffYZ < 0) diffYZ = -diffYZ;
        int diffXZ = x - z;
        // Normalize to absolute difference for XZ
        if (diffXZ < 0) diffXZ = -diffXZ;

        int alarm = 0;
        // Trigger alarm if any pair differs by more than 10
        if (diffXY > 10 || diffYZ > 10 || diffXZ > 10) {
            alarm = 2;
        }
        return alarm;
    }
}