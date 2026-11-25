// Character mapping helper: derives a candidate by scanning a small range
// This snippet demonstrates a simple loop with an early return for non-letter inputs

public class GetLowCaseLoop_M4 {
    public static char getLowCase(char c) {
        char t = 'f';
        // Initialize t to 'f' and iterate toward 'z' to locate a transformed input
        while(t <= 'z' && t != c - 'A' + 'a') {
            // Loop begins: compare and adjust t within the range
            if(c < 'F' || c > 'Z') {
                // If c is outside the A-Z range, there is no valid mapping
                return 0;
            }
            t++;
            // Move to the next candidate letter
        }
        // End of this iteration
        // Return the resulting character after the loop completes
        return t;
    }
}