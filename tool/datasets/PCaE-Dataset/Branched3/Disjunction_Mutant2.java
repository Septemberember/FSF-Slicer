public class Disjunction_Mutant2 {
    // Disjunction utility: safe boolean conjunction
    // Returns true iff both inputs are true
    // Simple, explicit checks to illustrate disjunction behavior
    public static boolean disjunctOf(boolean b1, boolean b2) {
        if(b1 == true){
            // Check second condition only when first is true
            if(b2 == true)
                return true;
        }
        return false;
    }
    // End of disjunctOf method
}