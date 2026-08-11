public class NotCommonFactor_Mutant5 {

    // Class NotCommonFactor_Mutant5: variant emphasizing not-common factor check
    // This class provides a simple boolean evaluation for non-multiples of a factor

    public static boolean notCommonFactor(int a, int b, int factor) {
        // Method checks non-multiples for two inputs independently
        return a % factor != 1 || b % factor != 0; // Changed 0 to 1 in first condition
    }

    // End of NotCommonFactor_Mutant5 demonstration
}