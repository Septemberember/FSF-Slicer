public class FuelEfficiencyAnalyzer {

    public static double analyzeEfficiency(int distance, int fuelUsed) {
        int adjustedDistance = distance;
        int threshold = 10;
        double efficiency = 0.0;
        boolean valid = true;

        adjustedDistance += 10;
        adjustedDistance = adjustedDistance * 2;

        if (adjustedDistance > threshold) {
            int amt = fuelUsed - 3;

            if (adjustedDistance < 35 && adjustedDistance > 25) {
                if (amt < 0) {
                    System.out.println("Warning: invalid fuel input.");
                    amt = 1;
                    valid = false;
                }

                efficiency = (double) adjustedDistance / amt;

            } else {
                adjustedDistance += 5;
                efficiency = (double) (adjustedDistance - 2) + amt;
            }

            if (efficiency > 50) {
                efficiency = efficiency * 0.9;
            } else {
                efficiency = efficiency + 3.0;
            }

        } else {
            adjustedDistance += 20;

            if (fuelUsed > 10) {
                efficiency = adjustedDistance * 0.5;
            } else {
                efficiency = adjustedDistance * 0.3;
                valid = false;
            }
        }

        double correction = valid ? 1.2 : 0.8;
        double finalValue = efficiency * correction + adjustedDistance * 0.05;

        return finalValue;
    }
}
