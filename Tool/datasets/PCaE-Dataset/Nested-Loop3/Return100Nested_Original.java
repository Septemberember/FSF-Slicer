/*
 * Utility: demonstrate a simple nested-loop computation.
 * This class contains a method that returns the constant value 100
 * by totaling 100 iterations across two nested loops.
 */

public class Return100Nested_Original {
    public static int return100 () {
        int res = 0;
        for(int i = 0; i < 10; i++) {
            for(int j = 0; j < 10; j++) {
                res = res + 1;
            }
        }
        return res;
    }
}