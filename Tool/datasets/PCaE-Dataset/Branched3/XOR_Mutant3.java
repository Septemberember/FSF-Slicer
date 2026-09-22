public class XOR_Mutant3 {
    // XOR operation implemented with conditional logic
    // Returns true when exactly one input is true
    public static boolean xor(boolean b1, boolean b2) {
        // Begin evaluation of operands
        if(b1 == true) {
            // If first operand is true, result depends on second
            if(b2 == true) {
                return true;
            }
            else {
                return false;
            }
        }
        else {
            // If first operand is false, XOR equals the second operand
            if(b2 == true) {
                return false;
            }
            else {
                return true;
            }
        }
    }
}
    // End of XOR_Mutant3 class