public class IsCommonFactor_Mutant5 {

    // This class provides a minimal example to test factor-related logic.
    // The isCommonFactor method checks divisibility of 'a' by 'factor' and evaluates 'b' against 'factor'.
    // The original code contains a simple mutation scenario for demonstration.
    
    public static boolean isCommonFactor(int a, int b, int factor) {
        return a % factor == 0 && b / factor == 0; // changed '%' to '/' at b % factor
    }
}