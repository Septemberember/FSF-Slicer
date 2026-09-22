public class ConvertToFahrenheit_Original {

    // Converts a temperature from Celsius to Fahrenheit using the standard formula
    // F = C * 1.8 + 32
    // This utility is intentionally straightforward and side-effect free.
    // Values are computed in double precision to preserve accuracy.

    /*
     * Celsius to Fahrenheit conversion utility.
     * Implements the classic equation: F = C * 1.8 + 32
     */
    public static double convertTemperature(double celsius) {
        return celsius * 1.80 + 32.00;
    }
}