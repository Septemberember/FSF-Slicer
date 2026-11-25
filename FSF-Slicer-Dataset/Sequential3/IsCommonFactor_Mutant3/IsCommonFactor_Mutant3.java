public class IsCommonFactor_Mutant3 {

    /**
     * IsCommonFactor utility with a simple predicate.
     * The predicate checks divisibility against a given factor for two inputs.
     * This variant demonstrates a straightforward boolean expression.
     */

    public static boolean isCommonFactor(int a, int b, int factor) {
        return a % factor == 0 && b % factor != 0; // changed '==' to '!=' at b % factor
    }
}