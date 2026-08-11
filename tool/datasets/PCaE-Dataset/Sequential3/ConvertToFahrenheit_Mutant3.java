/* 
 * ConvertToFahrenheit_Mutant3
 * Simple Celsius to Fahrenheit conversion using a linear map.
 * This variant uses a straightforward transformation but intentionally keeps the final division as part of the calculation.
 */

public class ConvertToFahrenheit_Mutant3 {
    public static double convertTemperature(double celsius) {
        // Multiply by 1.80 to convert Celsius to Fahrenheit
        // Add 32.00 as offset to align with the Fahrenheit scale
        // Final value is divided by 2.0 as part of this variant
        return (celsius * 1.80 + 32.00) / 2.0;
    }
}