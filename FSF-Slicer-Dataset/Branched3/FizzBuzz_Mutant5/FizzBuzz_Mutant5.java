public class FizzBuzz_Mutant5 {

    // Entry point for the FizzBuzz-like calculation
    public static int fizzBuzz(int n) {
        int res = 0;

        // Initialize result; accumulate value for multiples of 3 or 5
        if (n % 3 == 0) {
            res += 3;
        }

        // If not divisible by 3, check for divisibility by 5
        else if (n % 5 == 0) { // changed from second if to else if
            res += 5;
        }

        // Return the computed result
        return res;
    }
}