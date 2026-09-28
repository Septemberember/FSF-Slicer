public class Disjunction_Original {

    // Utility to determine if disjunction is true for boolean inputs.
    public static boolean disjunctOf(boolean b1, boolean b2) {

        // If the first operand evaluates to true, the disjunction holds.
        if(b1 == true)
            return true;

        // If the second operand evaluates to true, the disjunction holds.
        if(b2 == true)
            return true;

        // None of the operands are true; the disjunction is false.
        return false;
    }
}