// Wind compensation utility
// Generates a simple supplemental value based on wind speed.
public class WindCompensation_Mutant5 {
    public static int windCompensation(int windSpeed) {
        int compensation = 5;
        // Base compensation starts with 5 units.
        if (windSpeed > 20) {
            // For strong winds, add a quadratic-ish increase beyond 20.
            compensation += (windSpeed - 20) * 2;
        } else if (windSpeed > 10) {
            // Moderate winds add a linear increment for windSpeed above 10.
            compensation += windSpeed - 10;
        }
        return compensation;
    }
}