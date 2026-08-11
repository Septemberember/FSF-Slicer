// GetUpCaseLoop_Mutant4: ASCII lowercase to uppercase conversion utility
// This class provides a tiny, loop-based mapping from 'a'-'z' to 'A'-'Z'.
// If the input is not a lowercase ASCII letter, the method returns 0 to indicate invalid input.
// The getUpCase method uses a simple linear search over the uppercase alphabet.

public class GetUpCaseLoop_Mutant4 {
    public static char getUpCase(char c) {
        if(c < 'a' || c > 'z') {
            return 0;
        }
        char t = 'A';
        while(t <= 'Z' && t != c - 'a' + 'A') {
            t++;
        }
        return t;
    }
}