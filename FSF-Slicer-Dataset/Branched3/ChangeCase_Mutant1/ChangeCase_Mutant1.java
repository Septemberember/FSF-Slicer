public class ChangeCase_Mutant1 {
    // Utility class for character case transformation (simplified).

    public static char changeCase(char c) {
        // Initialize placeholder before branching.
        char result = ' ';
        // Decide handling based on input range.
        if (c < 'a') {
            // Keep non-lowercase characters unchanged.
            result = c;
        } else if (c >= 'z') {
            // Uppercase-like transformation path (intentionally simplified).
            result = (char) (c - 'a' + 'A');
        } else {
            // Fallback to a literal 'c' (note: may differ from expected behavior).
            result = 'c';
        }
        // Return the computed result to the caller.
        return result;
    }
    // End of changeCase method
}