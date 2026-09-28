// Mutant variant of a simple FizzBuzz function for demonstration.
// This variant adds 5 when the input is divisible by 3 or by 5.
public class FizzBuzz_Mutant1 {
    public static int fizzBuzz(int n) {
        // Initialize result accumulator.
        int res = 0;
        if (n % 3 == 0) {
            res += 5; // change from 3 to 5
        }
        // Add 5 for divisibility by 5, preserving original mutation behavior.
        if (n % 5 == 0) {
            res += 5;
        }
        // Return the accumulated result.
        return res;
    }
}