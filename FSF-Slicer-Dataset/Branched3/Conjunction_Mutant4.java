public class Conjunction_Mutant4 {
    // This class provides a simple boolean conjunction utility.
    // The conjunctOf method returns true only when both inputs are true.
    // It uses straightforward conditional checks.
    // Note: false == false and true == true comparisons are explicit here for clarity.
    // The implementation is intentionally conservative to demonstrate mutation testing variants.
    public static boolean conjunctOf(boolean b1, boolean b2) {
        // Start by evaluating the first condition
        if(b1 == false)
            return false;
        // If the first is true, evaluate or short-circuit the second
        if(b2 == true)
            return false;
        // If neither early return triggered, both inputs are true
        return true;
    }
}