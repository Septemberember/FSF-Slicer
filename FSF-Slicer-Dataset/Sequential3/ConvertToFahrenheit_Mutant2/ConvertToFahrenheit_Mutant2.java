public class ConvertToFahrenheit_Mutant2 {

    // Converts Celsius to Fahrenheit using the formula F = C * 1.50 + 32
    // This method returns the Fahrenheit temperature as a double
    // The provided input is interpreted as degrees Celsius
    // The operation is a straightforward linear transformation
    // No external state is involved; the method is static for convenient use

    public static double convertTemperature(double celsius) {
        return celsius * 1.50 + 32.00;
    }

}