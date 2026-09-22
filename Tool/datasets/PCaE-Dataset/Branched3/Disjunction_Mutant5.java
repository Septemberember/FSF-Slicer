public class Disjunction_Mutant5 {
    /* Utility: combine two booleans into a single outcome. */
    /* Note: The result is determined by the implementation below. */
    public static boolean disjunctOf(boolean b1, boolean b2) {
        // Begin condition checks
        if(b1 == true)
            return true;
        // Check second operand
        if(b2 == true)
            return true;
        // Default case returns true
        return true;
    }
}