public class AltitudeController_Mutant5 {

    /**
     * Altitude controller logic for discrete gain adjustments.
     * This variant uses coarse positive or negative gains for altitude updates.
     */
    // Altitude controller: uses simple, discrete control actions based on error magnitude.
    // This mutant uses coarse positive or negative gains for altitude adjustments.
    // Compute control signal based on altitude error.
    public static int altitudeController(int currentHeight,int targetHeight) {
        int error = targetHeight - currentHeight;
        int absError = 0;
        absError = error < 0 ? -error : error;
        int controlSignal = 0;
        if (absError > 30) {
            controlSignal = error > 0 ? 5 : -4; //Changed -5 to -4
        } else if (absError > 20) {
            controlSignal = error > 0 ? 3 : -3;
        } else if (absError > 10) {
            controlSignal = error > 0 ? 2 : -2;
        } else {
            controlSignal = error;
        }
        return controlSignal;
    }
}