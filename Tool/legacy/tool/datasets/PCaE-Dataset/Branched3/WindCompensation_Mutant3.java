public class WindCompensation_Mutant3 {
    // WindCompensation utility class
    public static int windCompensation(int windSpeed) {
        // Calculate compensation based on wind speed thresholds
        int compensation = 0;
        // Initialize compensation accumulator
        if (windSpeed > 20) {
            // First branch: strong winds
            compensation = (windSpeed - 20) * 2;
        } else if (windSpeed > 10) {
            // Secondary threshold for moderate winds
            compensation = (windSpeed - 10) * 2;
        }
        // End of conditional blocks
        return compensation;
        // Return computed compensation value
        // End of windCompensation method
    }
}