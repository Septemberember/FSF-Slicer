public class Return100Nested_Mutant3 {
    // This class exposes a computation that yields a fixed integer.
    // The computation consists of a 10x10 nested loop.
    // Each inner iteration adds 2 to the accumulator.
    // The resulting value is returned by return100().

    public static int return100 () {
        int res = 0;
        for(int i = 0; i < 10; i++) {
            for(int j = 0; j < 10; j++) {
                res = res + 2;
            }
        }
        return res;
    }
}