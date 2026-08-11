// Auto-generated mutant: minimal commentary added for readability
// This variant preserves behavior; only comments and blanks added
//
public class AltitudeController_Mutant2 {
    public static int altitudeController(int currentHeight,int targetHeight) {
        // Calculate the instantaneous height error as the difference between target and current
        // Positive error indicates we are below the target height
        // The magnitude of the error will guide the control signal strength
        int error = targetHeight - currentHeight;
        int absError = 0;
        // Absolute value of error simplifies threshold comparisons
        absError = error < 0 ? -error : error;
        int controlSignal = 1; //Changed 0 to 1
        // Initial value set above; larger errors require stronger correction
        if (absError > 30) {
            controlSignal = error > 0 ? 5 : -5;
        } else if (absError > 20) {
            controlSignal = error > 0 ? 3 : -3;
        } else if (absError > 10) {
            controlSignal = error > 0 ? 2 : -2;
        } else {
            controlSignal = error;
        }
        // End of altitude adjustment calculation
        return controlSignal;
    }
    // End of altitudeController method
}
 // End of AltitudeController_Mutant2