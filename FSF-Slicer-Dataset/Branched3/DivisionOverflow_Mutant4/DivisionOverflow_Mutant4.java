public class DivisionOverflow_Mutant4 {
    // Test scaffolding: ensure safe handling of division by non-zero denominators.
    // The following path performs an integer division when denominator is non-zero.
    public static int division_test_fail_overflow(int nom, int denom) {
        //~should_fail
        // Guard: denom should be non-zero to avoid ArithmeticException.
        if (denom != 0) { //add a check for denominator to be non-zero
            int tmp = nom / denom;
            return tmp;
        }
        // If denom is zero, return a neutral result.
        return 0;
    }
}