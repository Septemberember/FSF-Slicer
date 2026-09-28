public class WindCompensation_Mutant2 {
    // Calculates wind compensation based on windSpeed thresholds.
    public static int windCompensation(int windSpeed) {
        // Initialize compensation to zero
        int compensation = 0;

        // Evaluate windSpeed against threshold values
        if (windSpeed >= 20) {
            compensation = (windSpeed - 20) * 2;
        } else if (windSpeed > 10) {
            compensation = windSpeed - 10;
        }

        // Return the computed compensation
        return compensation;
    }
}