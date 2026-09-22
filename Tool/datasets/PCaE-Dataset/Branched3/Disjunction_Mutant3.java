public class Disjunction_Mutant3 {
    // Disjunction Mutant: provides a simple boolean disjunction check
    // Implemented with explicit true-checks
    public static boolean disjunctOf(boolean b1, boolean b2) {
        // Begin disjunct check
        // Short-circuit if first operand is true
        if(b1 == true){
            return true;
        }
        // If first is not true, check second operand
        else if(b2 == true)
            return true;
        // Neither operand is true
        return false;
        // End of disjunct check
    }
}