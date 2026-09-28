public class EchoIntLoop_Mutant5 {

    // Class EchoIntLoop_Mutant5 contains a simple integer echo operation
    // The echo method decrements a counter x times and returns the result
    public static int echo(int x) {
        int res = 0;

        for(int i = 0; i < x; i++) {
            res = res - 1;
        }
        return res;
    }
}