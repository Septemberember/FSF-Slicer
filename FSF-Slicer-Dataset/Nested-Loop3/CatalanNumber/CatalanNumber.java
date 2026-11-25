// Source: adapted implementation and specifications from the independent 236-program maintenance corpus, Nested Loop/CatalanNumber/CatalanNumber.verified.java.
public class CatalanNumber {

    public static int catalanNumber(int num) {
        if (num < 0 || num > 19) {
            return -1;
        }
        int[] catalan = new int[num + 1];
        catalan[0] = 1;

        for (int i = 1; i <= num; i++) {
            catalan[i] = 0;

            for (int j = 0; j < i; j++) {
                catalan[i] += catalan[j] * catalan[i - j - 1];
            }
        }
        return catalan[num];
    }
}
