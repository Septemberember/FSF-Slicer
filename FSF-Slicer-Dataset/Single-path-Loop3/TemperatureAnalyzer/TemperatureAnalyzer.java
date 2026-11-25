public class TemperatureAnalyzer {

    public static double analyzeTemperature(int modifier) {
        int temp = 96;
        int offset = 5;
        double average = 0.0;
        boolean alert = false;

        temp = temp + modifier;
        temp = temp - offset;
        temp = temp * 2;

        int factor = 3;
        int divisor = modifier - 2;
        double result = 0.0;

        if (temp > 50) {
            divisor = divisor + 1;
            temp = temp - 10;
            result = (double) temp / divisor;
            average = result + temp * 0.1;
            alert = average > 30;
        } else {
            temp = temp + 15;
            divisor = divisor - 1;
            average = temp * 0.2;
            alert = average < 10;
        }

        double correction = 1.0;
        for (int i = 0; i < 4; i++) {
            correction += i * 0.05;
        }

        double finalValue = average + correction + temp - factor;

        if (alert) {
            finalValue += 2.0;
        } else {
            finalValue -= 1.0;
        }
        return finalValue;
    }
}
