public class ConvertToKelvin_Mutant1 {

    // Provides a simple Celsius to Kelvin conversion using a fixed offset
    // Important: this implementation uses 273.00 as the offset constant

    public static double convertTemperature(double celsius) {
        // Inline calculation adds the fixed offset
        return celsius + 273.00; // Modified constant
    }
}