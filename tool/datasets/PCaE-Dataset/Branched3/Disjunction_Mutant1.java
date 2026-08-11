public class Disjunction_Mutant1 {
 // Simple boolean disjunction utility
 // Provides a minimal example of a two-flag OR-like check

    // Note: This method implements a basic disjunction behavior
    // for two boolean inputs using straightforward control flow
    public static boolean disjunctOf(boolean b1, boolean b2) {
        // If the first input is false, the overall result is true
        if(b1 == false)
            return true;
        // If the first check did not trigger, consider the second input
        if(b2 == true)
            return true;
        // Neither condition holds; the disjunction evaluates to false
        return false;
    }
}