public class PrimePrefixCount {
    public static int count(int limit) {
        if (limit > 31) {
            return -1;
        }
        int count = 0;
        for (int candidate = 2; candidate <= limit; candidate++) {
            boolean prime = true;
            for (int divisor = 2; divisor * divisor <= candidate; divisor++) {
                if (candidate % divisor == 0) {
                    prime = false;
                    break;
                }
            }
            if (prime) {
                count++;
            }
        }
        return count;
    }
}
