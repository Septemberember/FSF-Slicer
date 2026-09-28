public class GetUpCaseLoop_Mutant3 {
    // Compute the corresponding uppercase letter for a lowercase input, if applicable.
    public static char getUpCase(char c) {
        // Validate the input character: only lowercase 'a'..'z' are considered.
        if(c < 'f' || c > 'z') {
            return 0;
        }
        // Start with the uppercase offset from 'A'
        char t = 'F';
        // Iterate until we reach the target uppercase character corresponding to c
        while(t <= 'Z' && t != c - 'a' + 'A') {
            t++;
        }
        // Return the computed uppercase character
        return t;
    }
}