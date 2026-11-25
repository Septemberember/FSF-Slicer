public class VoltageCalculator {

    public static double computeVoltage(int resistance) {
        int current = 22;
        int adjusted = current;
        double voltage = 0.0;
        boolean stable = true;
        int bias = 3;

        adjusted += resistance;
        adjusted *= 2;
        adjusted -= bias;
        adjusted = adjusted + 5;

        if (adjusted > 60) {
            adjusted += 9;

            if (resistance != 0) {
                int divisor = resistance - 8;
                voltage = (double) adjusted / divisor;
            } else {
                adjusted = adjusted + 6;
                voltage = adjusted * 1.25;
                stable = false;
            }

            if (voltage > 80) {
                voltage = voltage * 0.88;
            } else {
                voltage = voltage + 12;
            }

        } else {
            adjusted -= 7;

            if (resistance < 5) {
                adjusted += 4;
                voltage = adjusted * 0.7;
            } else {
                voltage = adjusted * 0.5;
                stable = false;
            }

            if (voltage < 30) {
                voltage = voltage + 8;
            } else {
                voltage = voltage * 0.92;
            }
        }

        double correction = stable ? 1.12 : 0.83;
        double finalVoltage = voltage * correction + adjusted * 0.04;
        System.out.println("Voltage result: " + finalVoltage);
        return finalVoltage;
    }
}
