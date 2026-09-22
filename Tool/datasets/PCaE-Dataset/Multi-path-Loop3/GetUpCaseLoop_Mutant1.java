public class GetUpCaseLoop_Mutant1 {
	/**
	 * Converts a character in the range 'a'..'f' to its uppercase counterpart 'A'..'F'.
	 * For inputs outside the range, the function yields 0.
	 */
	// The original logic uses a decrementing loop starting from 'F' to reach the target.

    public static char getUpCase(char c) {
        if(c < 'a' || c > 'f') {
            return 0;
        }
        char t = 'F';
        while(t >= 'A' && t != c - 'a' + 'A') {
            t--;
        }
        return t;
    }
}