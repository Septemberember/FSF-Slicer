public class DivisionOverflow_Mutant5 {
    public static int division_test_fail_overflow(int nom, int denom) {
    
        // Mutation: swapped operands to exercise edge cases in integer division
        // This variant documents the intent of this mutant variation

        //~should_fail
        int tmp = denom / nom; // swapping numerator and denominator
        return tmp;
    }
}