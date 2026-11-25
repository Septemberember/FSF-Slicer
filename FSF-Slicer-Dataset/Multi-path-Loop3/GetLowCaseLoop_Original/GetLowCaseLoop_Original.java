public class GetLowCaseLoop_Original {
    // GetLowCase: determine the lowercase-like proxy for an ASCII letter
    
    // Helper: maps an input character to its lowercase equivalent when valid
    public static char getLowCase(char c) {
        char t = 'z';
        while(t >= 'a' && t != c - 'A' + 'a') {
            // If the current character is not an uppercase ASCII letter, mapping is not applicable
            if(c < 'A' || c > 'Z') {
                return 0;
            }
            // Step downward to locate a matching lowercase proxy
            t--;
        }
        return t;
    }
}