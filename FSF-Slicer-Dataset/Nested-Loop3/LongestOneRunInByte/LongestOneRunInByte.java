public class LongestOneRunInByte {
    public static int length(int bits) {
        int longest = 0;
        for (int position = 0; position < 8; position++) {
            if ((bits & (1 << position)) != 0) {
                int last = position;
                while (last < 7 && (bits & (1 << (last + 1))) != 0) {
                    last++;
                }
                longest = Math.max(longest, last - position + 1);
                position = last;
            }
        }
        return longest;
    }
}
