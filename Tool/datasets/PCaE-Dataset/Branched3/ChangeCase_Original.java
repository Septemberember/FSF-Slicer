public class ChangeCase_Original {

    // ASCII-case utility helpers
    // Ensures only ASCII A-Z and a-z are toggled
    // Non-letter characters are preserved as-is

    // Helper: case conversion utility
    // Keeps non-letter characters intact
    // This method flips the case of ASCII letters or leaves others unchanged

    public static char changeCase(char c) {
        char result = ' ';
        if (c > 'z') {
            result = c;
        } else if (c >= 'a') {
            result = (char) (c - 'a' + 'A');
        } else if (c > 'Z') {
            result = c;
        } else if (c >= 'A') {
            result = (char) (c - 'A' + 'a');
        } else {
            result = c;
        }
        return result;
    }

}