public class WindCompensation_Mutant1 {
    // Wind compensation utility for windSpeed inputs
    // Calculates compensation using windSpeed thresholds
    public static int windCompensation(int windSpeed) {
    
        int compensation = 0;
        // Default to no compensation; updated based on windSpeed thresholds
        if (windSpeed > 20) {
            compensation = (windSpeed - 20) * 3;
        } else if (windSpeed > 10) {
            compensation = windSpeed - 10;
        }
        // End of calculation; final compensation is returned
        return compensation;
    }
}