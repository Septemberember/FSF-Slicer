public class ChangeCase_Mutant5 {

    // Utility: ASCII-based case conversion helper
    // Converts between lowercase and uppercase for English letters.
    // Non-letter characters are left unchanged.
    // This method uses simple arithmetic with the 'a', 'A', 'z', and 'Z' boundaries.


    public static char changeCase(char c) {
        char result = ' ';
        // Initialize result with a safe default; actual value is set by the conditional branches.
        if (c > 'z') {
            result = c;
        } else if (c >= 'a') {
            result = (char) ('a' - 'A' + c);
        } else if (c > 'Z') {
            result = c;
        } else if (c >= 'A') {
            result = (char) (c - 'A' + 'a');
        } else {
            result = c;
        }
        // End of changeCase method.
        return result;
    }

}