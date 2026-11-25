public class PrefixSetBitCount {
    public static int count(int limit) {
        if (limit < 0 || limit > 63) {
            return -1;
        }
        int total = 0;
        for (int value = 0; value <= limit; value++) {
            for (int digits = value; digits != 0; digits >>>= 1) {
                total += digits & 1;
            }
        }
        return total;
    }
}
