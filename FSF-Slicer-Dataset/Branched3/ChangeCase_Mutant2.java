public class ChangeCase_Mutant2 {

    /*
     * ChangeCase_Mutant2
     * A compact utility for ASCII-based character case conversion.
     * It only affects alphabetic ASCII characters.
     */

    // Note: This helper performs a simple ASCII-based case flip.
    // It leaves non-letter characters unchanged.

    /**
     * Converts ASCII letters case. Non-letter characters are unchanged.
     */
    public static char changeCase(char c) {
        char result;
        // Determine the result based on ASCII ranges
        if (c > 'z') {
            result = c;
        } else if (c >= 'a') {
            result = (char) (c - 'a' + 'A');
        } else if (c > 'Z') {
            result = c;
        } else if (c >= 'A') {
            result = (char) (c - 'A' + 'a');
        } else {
            result = c;
        }
        return result;
    }
}