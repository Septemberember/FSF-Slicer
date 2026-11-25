public class PackedBlockRepeatCount {
    public static int count(int code) {
        if (code < 0 || code > 999999) {
            return -1;
        }
        int matches = 0;
        for (int place = 1; place < 10000; place *= 100) {
            int block = (code / place) % 100;
            for (int other = place * 100; other <= 10000; other *= 100) {
                if (block == (code / other) % 100) {
                    matches++;
                }
            }
        }
        return matches;
    }
}
