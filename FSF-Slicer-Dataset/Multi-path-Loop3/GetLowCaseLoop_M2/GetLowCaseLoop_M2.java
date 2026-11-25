public class GetLowCaseLoop_M2 {
    // Lightweight utility class illustrating a constrained lowercase-like computation.
    public static char getLowCase(char c) {
        char t = 'f';
        // t is initialized to the ASCII value for 'f' to start the comparison.
        while(t >= 'a' && t != c - 'A' + 'a') {
            if(c < 'A' || c > 'F') {
                return 0;
            }
            t--;
        }
        // Return the computed character value.
        return t;
    }
    // End of getLowCase method.
}
 // End of class GetLowCaseLoop_M2.