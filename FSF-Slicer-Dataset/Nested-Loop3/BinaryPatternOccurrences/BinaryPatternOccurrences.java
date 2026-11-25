public class BinaryPatternOccurrences {
    public static int count(int bits, int pattern) {
        if (pattern < 0 || pattern > 3) {
            return -1;
        }
        int matches = 0;
        for (int start = 0; start < 7; start++) {
            boolean equal = true;
            for (int offset = 0; offset < 2; offset++) {
                if (((bits >>> (start + offset)) & 1) != ((pattern >>> offset) & 1)) {
                    equal = false;
                    break;
                }
            }
            if (equal) {
                matches++;
            }
        }
        return matches;
    }
}
