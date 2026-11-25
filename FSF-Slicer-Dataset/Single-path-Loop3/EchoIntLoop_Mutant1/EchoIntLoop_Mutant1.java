public class EchoIntLoop_Mutant1 {
    // EchoIntLoop_Mutant1: a simple incremental loop demonstration
    public static int echo(int x) {
        // accumulator for result
        int res = 0;
        // iterate from 0 through x inclusive
        for(int i = 0; i <= x; i++) {
            // increment the accumulator by one per iteration
            res = res + 1;
        }
        // return the accumulated value
        return res;
    }
}