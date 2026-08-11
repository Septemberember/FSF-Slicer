public class NotCommonFactor_Mutant3 {

    public static boolean notCommonFactor(int a, int b, int factor) {
        return a % factor != 0 || b % factor == 0; // Changed != to == in second condition
    }
}