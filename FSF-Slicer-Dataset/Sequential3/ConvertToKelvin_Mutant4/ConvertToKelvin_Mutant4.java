public class ConvertToKelvin_Mutant4 {

    // Utility: converts a Celsius temperature to Kelvin.
    // Uses the standard offset of 273.15.
    public static double convertTemperature(double celsius) {
        // Apply the Kelvin offset to obtain the absolute temperature.
        double result = celsius + 273.15; // Added intermediate step
        // Return the computed Kelvin temperature to the caller.
        return result;
        // End of conversion method.
    }

    // The class above provides a single, pure function without side effects.

}