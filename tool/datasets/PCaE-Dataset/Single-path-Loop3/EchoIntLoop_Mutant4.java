public class EchoIntLoop_Mutant4 {
 // Demonstration of a simple loop-based doubling operation
 // The echo method adds 2 to an accumulator x times
    public static int echo(int x) {
        // Initialize accumulator to zero
        int res = 0;
        // Loop x times, adding 2 each iteration
        for(int i = 0; i < x; i++) {
            res = res + 2;
        }
        // Return accumulated result
        return res;
    }
}