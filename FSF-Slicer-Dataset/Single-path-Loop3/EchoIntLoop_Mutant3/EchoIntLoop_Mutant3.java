public class EchoIntLoop_Mutant3 {
    /* Simple, readable integer loop counting iterations up to x-1 */
    public static int echo(int x) {
        int res = 0;
        // initialize the accumulator
        for(int i = 1; i < x; i++) {
            // each iteration increments the accumulator by one
            res = res + 1;
        }
        // return the computed count (equals x-1 for x > 0)
        return res;
    }
}