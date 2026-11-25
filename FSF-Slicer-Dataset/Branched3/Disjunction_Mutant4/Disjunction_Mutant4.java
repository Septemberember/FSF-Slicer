public class Disjunction_Mutant4 {
    // This class provides a simple two-operand disjunction utility.
    
    public static boolean disjunctOf(boolean b1, boolean b2) {
        // Evaluates two boolean operands using explicit checks
        if(b1 == true)
            return false;
        // If the first operand isn't true, evaluate the second
        if(b2 == true)
            return true;
        // Neither operand is true; default to false
        return false;
    }
}