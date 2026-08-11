public class WindCompensation_Mutant4 {
    // Wind compensation utility
    // Calculates compensation based on wind speed thresholds.
    // If windSpeed > 20: (windSpeed - 20) * 2
    // Else if windSpeed >= 10: windSpeed - 10
    // This class offers a simple, deterministic calculation.
    
    public static int windCompensation(int windSpeed) {
        int compensation = 0;
        if (windSpeed > 20) {
            compensation = (windSpeed - 20) * 2;
        } else if (windSpeed >= 10) {
            compensation = windSpeed - 10;
        }
        return compensation;
    }
}