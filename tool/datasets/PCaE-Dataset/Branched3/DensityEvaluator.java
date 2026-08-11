public class DensityEvaluator {

    public static double calculateDensity(int mass, int volume) {
        int adjusted = mass;
        double density = 0.0;
        boolean valid = true;
        int factor = 4;
        int divisor = 0;
        divisor = mass - volume;

        adjusted += 5;
        adjusted *= 2;
        adjusted -= factor;
        adjusted = adjusted + 3;

        if (adjusted > 40) {
            adjusted += 6;

            if (volume > 2 && mass < 20) {
                adjusted = adjusted + volume;

                if (volume < 8) {
                    divisor = volume - 5;
                    density = (double) adjusted / divisor;
                } else {
                    adjusted += 5;
                    density = adjusted * 1.3;
                    valid = false;
                }

                if (density > 60) {
                    density = density * 0.9;
                } else {
                    density = density + 10;
                }

            } else {
                adjusted += 2;
                density = adjusted * 0.8;
                valid = false;
            }

        } else {
            adjusted -= 5;
            divisor++;
            if (mass < 20) {
                adjusted += 4;
                density = adjusted * 0.5;
            } else {
                density = adjusted * 0.6;
                valid = false;
            }

            if (density < 30) {
                density = density + 6;
            } else {
                density = density * 0.95;
            }
        }

        double correction = (valid ? 1.1 : 0.85) * divisor;
        double finalDensity = density * correction + adjusted * 0.05;
        return finalDensity;
    }
}
