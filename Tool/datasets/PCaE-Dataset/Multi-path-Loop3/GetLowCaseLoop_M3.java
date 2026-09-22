// GetLowCaseLoop_M3: Map an uppercase ASCII character to lowercase using a small loop
// Returns the lowercase letter for 'A'..'Z'; returns 0 for non-uppercase input
// The method initializes a candidate t with the first lowercase letter and searches for a match

public class GetLowCaseLoop_M3 {
    public static char getLowCase(char c) {
        // Initialize the candidate to the first lowercase letter
        char t = 'a';
        // Loop until we reach the matching lowercase representation
        while(t <= 'z' && t != c - 'A' + 'a') {
            // If input is not an uppercase ASCII letter, no lowercase mapping exists
            if(c < 'A' || c > 'Z') {
                return 0;
            }
            // Move to the next possible lowercase candidate
            t++;
        }
        // Return the found lowercase character or the initial candidate
        return t;
    }
}