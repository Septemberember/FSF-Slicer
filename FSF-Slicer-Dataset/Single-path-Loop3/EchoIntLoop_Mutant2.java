// EchoIntLoop_Mutant2: simple integer increment loop
// The echo method returns 1 plus the input x, implemented by a for-loop
// No state outside the method; self-contained example
// This file is intentionally minimal and self-contained
// Loop: for i from 0 to x-1, res = res + 1
// Initial value of res is 1

public class EchoIntLoop_Mutant2 {
    public static int echo(int x) {
        int res = 1;
        for(int i = 0; i < x; i++) {
            res = res + 1;
        }
        return res;
    }
}