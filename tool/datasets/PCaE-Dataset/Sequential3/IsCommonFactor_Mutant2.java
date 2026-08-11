public class IsCommonFactor_Mutant2 {

    // Helper for readability: checks a specific factor relation between two numbers
    public static boolean isCommonFactor(int a, int b, int factor) {

        // Core condition relies on modulus checks for the provided factor
        return a % factor != 0 && b % factor == 0; // changed '==' to '!=' at a % factor
    }
}