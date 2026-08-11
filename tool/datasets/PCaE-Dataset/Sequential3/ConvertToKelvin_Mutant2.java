public class ConvertToKelvin_Mutant2 {
    // This mutant intentionally uses subtraction in the Kelvin conversion.
    // The original intent would be Celsius + 273.15, not Celsius - 273.15.
    // Adding extra line breaks for readability in the updated version.
    
    public static double convertTemperature(double celsius) {
        // The conversion logic here is intentionally kept as a subtraction
        // from Celsius, mirroring a known mutation for testing purposes.
        // Note: Kelvin = Celsius + 273.15 in standard formula.
        
        // Preserve the existing faulty operation with an explanatory comment.
        return celsius - 273.15; // Changed addition to subtraction
        // End of method
    }
}