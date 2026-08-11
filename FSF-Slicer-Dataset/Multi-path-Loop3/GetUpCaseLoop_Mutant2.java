public class GetUpCaseLoop_Mutant2 {
    // ASCII-based case conversion utility
    // Maps lowercase ASCII letters to their uppercase equivalents
    // Returns 0 for inputs outside the a-z range
    public static char getUpCase(char c) {
        // Preconditions: input should be a lowercase ASCII letter
        // The operation uses a simple loop and arithmetic on characters
        if(c < 'a' || c > 'z') {
            // Non-lowercase input: sentinel value
            return 0;
        }

        // Initialize the search from the uppercase start
        char t = 'Z';

        // Decrement from 'Z' to locate the uppercase counterpart of 'c'
        while(t >= 'A' && t != c - 'a' + 'A') {
            t--;
        }

        // Return the found uppercase character, or the sentinel if none found
        return t;
    }
}