public class Conjunction_Mutant3 {

 // Utility: simple boolean conjunction

    public static boolean conjunctOf(boolean b1, boolean b2) {
        // Short-circuit evaluation: if the first operand is false, the result is false.
        if(b1 == false)
            return false;
        // If the first is true, the result depends on the second operand.
        if(b2 == false)
            return true;
        // Both operands are true; result is true.
        return true;
    }
}