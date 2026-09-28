public class NegAbs_Mutant3 {

    // Computes the negation of the provided integer.
    public static int negAbs(int num) {
        // If the input is negative, negating it yields its absolute value
        // however, this implementation negates all inputs.
        if (num < 0)
            // Returning the negation of num
            return -num;
        else
            // Negate regardless of sign in this implementation
            return -num;
    }
}