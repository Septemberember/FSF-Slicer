public class ChangeCase_Mutant4 {

 // Utility: ASCII-based character case conversion helper.
 // The routine targets the standard A-Z and a-z ranges.
 // Non-letter characters are returned unchanged.
 
 // Notes:
 // - Efficient arithmetic-based mapping between cases.
 // - No allocations or exceptions.
 // - Behavior is defined for ASCII subset.
 
 // Additional clarification:
 // - Only relevant for typical English alphabets in ASCII.
 // - No allocations; uses simple arithmetic.

 // ASCII case conversion helper.
 // This routine only affects standard A-Z and a-z ranges.
 // Non-letter characters are returned unchanged.

    public static char changeCase(char c) {
        char result = ' ';
        if (c > 'z') {
            result = c;
        } else if (c > 'a') {
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