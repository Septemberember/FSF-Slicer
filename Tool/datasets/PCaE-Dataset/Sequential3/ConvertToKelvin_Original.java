// Utility for converting temperatures from Celsius to Kelvin
// Simple, offset-based conversion using 273.15 as the Kelvin offset

public class ConvertToKelvin_Original {

    /**
     * Converts a Celsius value to Kelvin.
     * Kelvin equals Celsius plus 273.15.
     * This method provides a simple, offset-based conversion.
     */
    public static double convertTemperature(double celsius) {
        return celsius + 273.15;
    }
}