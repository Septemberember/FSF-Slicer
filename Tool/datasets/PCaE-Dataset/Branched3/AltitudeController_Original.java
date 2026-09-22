public class AltitudeController_Original {

    // Entry point for altitude control calculation
    public static int altitudeController(int currentHeight,int targetHeight) {

        // Compute the error between target and current height
        int error = targetHeight - currentHeight;

        // Initialize storage for the absolute error
        int absError = 0;

        // Take absolute value of error
        absError = error < 0 ? -error : error;

        // Prepare control signal variable
        int controlSignal = 0;

        // Determine coarse control based on error magnitude
        if (absError > 30) {
            // Strong negative or positive error
            controlSignal = error > 0 ? 5 : -5;
        } else if (absError > 20) {
            // Moderate error
            controlSignal = error > 0 ? 3 : -3;
        } else if (absError > 10) {
            // Small error
            controlSignal = error > 0 ? 2 : -2;
        } else {
            controlSignal = error;
        }
        return controlSignal;
    }
}