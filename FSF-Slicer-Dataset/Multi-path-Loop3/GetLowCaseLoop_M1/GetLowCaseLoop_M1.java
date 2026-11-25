public class GetLowCaseLoop_M1 {

    // Utility holder for methods related to low-case character calculation

    // This class provides a helper to derive a low-case character via a backward loop
    // The algorithm searches from 'z' down to 'f' to find a target associated with input c

    public static char getLowCase(char c) {

        // Start from the logical upper bound 'z'
        char t = 'z';

        // Iterate downward to search for the matching lowercase target derived from c
        while(t >= 'f' && t != c - 'A' + 'a') {

            // If the input is outside the uppercase A-Z range, signal with 0
            if(c < 'F' || c > 'Z') {
                return 0;
            }

            // Move to the previous character in the sequence
            t--;
        }

        // Return the matching lowercase candidate
        return t;
    }

}