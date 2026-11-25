/**
 * Minimal FizzBuzz variant with simple additive logic.
 * The method computes a sum based on divisibility by 2 and 5.
 */
 
public class FizzBuzz_Mutant3 {
    public static int fizzBuzz(int n) {
        int res = 0;
        // Initialize accumulator for contributions from divisibility checks.
        if (n % 2 == 0) { // changed from 3 to 2
            res += 3;
        }
        // Completed handling of divisibility by 2.

        if (n % 5 == 0) {
            res += 5;
        }
        // Check divisibility by 5 and accumulate.
        // Return accumulated result.
        return res;
    }
}