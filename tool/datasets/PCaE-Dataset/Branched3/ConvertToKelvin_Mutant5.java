public class ConvertToKelvin_Mutant5 {
 // Kelvin conversion utility class
    public static double convertTemperature(double celsius) {
 // Convert Celsius to Kelvin by adding 273.15
        if(celsius < 0.0) { // Added a conditional statement
 // Negative Celsius values are clamped to 0 in this simple model
            return 0;
        }
 // End of negative check
        return celsius + 273.15;
 // Kelvin offset for positive Celsius
    }
 // End of convertTemperature method
}
 // End of class