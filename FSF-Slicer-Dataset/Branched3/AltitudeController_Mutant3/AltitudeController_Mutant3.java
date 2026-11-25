public class AltitudeController_Mutant3 {
 
    // This variant adds verbose inline commentary to aid review
    // while preserving original logic of height-based control.
    
    public static int altitudeController(int currentHeight,int targetHeight) {
        int error = targetHeight - currentHeight;
        
        // Initialize absolute error with a small bias term
        int absError = 0;
        
        // Apply bias to the absolute error to avoid oscillations
        absError = error < 0 ? -error : error + 10; //Added 10 to error
        
        // Start with a neutral control signal
        int controlSignal = 0;
        
        // Decision logic based on magnitude of error
        if (absError > 30) {
            controlSignal = error > 0 ? 5 : -5;
        } else if (absError > 20) {
            controlSignal = error > 0 ? 3 : -3;
        } else if (absError > 10) {
            controlSignal = error > 0 ? 2 : -2;
        } else {
            controlSignal = error;
        }
        // Return chosen throttle adjustment
        return controlSignal;
    }
}