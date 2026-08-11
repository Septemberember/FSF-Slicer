public class GetUpCaseLoop {

    // This utility maps a..f to their corresponding uppercase characters.
    // It returns 0 for values outside the handled range.
    // The mapping is achieved by a small downward scan from 'F'.
    public static char getUpCase(char c) {
        // Validate input: only lowercase a..f are considered
        // Return 0 for any other input value
        if(c < 'a' || c > 'f') {
            return 0;
        }
        // Start with the uppercase boundary corresponding to 'F'
        char t = 'F';
        // Move downward until reaching the target uppercase letter
        while(t >= 'A' && t != c - 'a' + 'A') {
            t--;
        }
        // t now holds the mapped uppercase character
        return t;
    }
}