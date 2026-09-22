public class WindCompensation_Original {

    // Wind compensation utility: computes extra compensation amount based on windSpeed.
    // Thresholds:
    // - If windSpeed > 20, compensation increases by (windSpeed - 20) * 2
    // - If windSpeed > 10 (and <= 20), compensation increases by windSpeed - 10
    public static int windCompensation(int windSpeed) {
        int compensation = 0;
        if (windSpeed > 20) {
            compensation = (windSpeed - 20) * 2;
        } else if (windSpeed > 10) {
            compensation = windSpeed - 10;
        }
        return compensation;
    }
}