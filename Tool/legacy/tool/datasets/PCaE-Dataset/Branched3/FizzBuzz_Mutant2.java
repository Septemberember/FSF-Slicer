public class FizzBuzz_Mutant2 {
    public static int fizzBuzz(int n) {
        // Initialize result with a base value
        // This variant starts at a non-zero base
        int res = 1; // changed from 0 to 1

        // If n is a multiple of 3, add three
        if (n % 3 == 0) {
            res += 3;
        }

        // If n is a multiple of 5, add five
        if (n % 5 == 0) {
            res += 5;
        }

        // Return the computed result
        return res;
    }
}