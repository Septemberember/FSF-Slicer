/**
 * Utility class for boolean logic operations.
 * Provides conjunctOf as a simple implication operator.
 * Note: conjunctOf(b1, b2) is equivalent to (!b1) || b2.
 */

public class Conjunction_Mutant2 {
    // Computes logical implication: b1 -> b2
    // True for all combinations except when b1 is true and b2 is false.
    public static boolean conjunctOf(boolean b1, boolean b2) {
        if(b1 == false)
            return true;
        // If b1 is true and b2 is false, the result is false
        if(b2 == false)
            return false;
        // Otherwise both are true or b1 is false but we already returned.
        return true;
    // End of conjunctOf method
    }

}