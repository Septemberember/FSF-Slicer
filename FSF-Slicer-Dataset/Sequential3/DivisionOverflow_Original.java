public class DivisionOverflow_Original {

    // Demonstration: integer division in Java
    // This class contains a single static method that performs
    // a straightforward division of nom by denom.

    /**
     * Performs integer division of nom by denom.
     * Note: division by zero will throw ArithmeticException.
     */
    public static int division_test_fail_overflow(int nom, int denom) {
        // The following line computes the quotient of nom divided by denom.
        int tmp = nom / denom;
        // Return the computed quotient to the caller.
        return tmp;
    }
}