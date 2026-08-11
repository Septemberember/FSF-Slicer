public class Conjunction_Mutant1 {

    // This method implements a basic conjunction with explicit guards
    public static boolean conjunctOf(boolean b1, boolean b2) {

        // Short-circuit: evaluate based on the first operand
        if(b1 == true)
            return false;

        // Short-circuit: if the second operand is false, the conjunction is false
        if(b2 == false)
            return false;

        // If both operands are true, the conjunction evaluates to true
        return true;
    }
}