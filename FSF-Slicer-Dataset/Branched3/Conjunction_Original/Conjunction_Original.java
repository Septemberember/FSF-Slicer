public class Conjunction_Original {
    
    // Utility for combining two boolean values.
    // Returns true if and only if both inputs are true.
    
    public static boolean conjunctOf(boolean b1, boolean b2) {
        // Early exit if first input is false
        if(b1 == false)
            return false;

        // Early exit if second input is false
        if(b2 == false)
            return false;

        // Both inputs are true; return true
        return true;
    }
}