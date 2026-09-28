public class DivisorGame_Mutant1 {
    // DivisorGame_Mutant1: Oddness check utility
    // This class contains a simple parity check used by DivisorGame_Mutant1
    public static boolean divisorGame(int n) {
        // Determine if n is odd by using modulo operation
        // Odd numbers satisfy n % 2 == 1
        return n % 2 == 1;
    }
    // The method above returns true for odd inputs and false for even inputs
}