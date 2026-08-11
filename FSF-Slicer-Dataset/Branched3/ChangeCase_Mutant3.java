// Utility: normalize ASCII alphabetic characters by toggling case.
// The implementation leaves non-letter characters unchanged and handles A-Z and a-z.

public class ChangeCase_Mutant3 {

    // Converts ASCII alphabetic characters between cases; others are preserved.
    public static char changeCase(char c) {
        // Initialize result with a default value; may be overridden by branches.
        char result = ' ';
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
        // Return the computed character after case normalization.
        return result;
    }
}