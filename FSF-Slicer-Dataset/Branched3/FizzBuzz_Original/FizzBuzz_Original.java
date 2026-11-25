// FizzBuzz_Original: returns 3 for multiples of 3, 5 for multiples of 5, and their sum if both.

public class FizzBuzz_Original {

    // Computes a simple sum based on divisibility by 3 and 5.
    public static int fizzBuzz(int n) {
        // accumulator for the computed result
        int res = 0;
        if (n % 3 == 0) {
            // add 3 when n is a multiple of 3
            res += 3;
        }
        if (n % 5 == 0) {
            // add 5 when n is a multiple of 5
            res += 5;
        }
        // final accumulated value is returned
        return res;
    }
}