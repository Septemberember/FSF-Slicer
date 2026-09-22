public class XOR_Original {
    // XOR_Original exposes a single static method for exclusive-or behavior
    public static boolean xor(boolean b1, boolean b2) {
        // Evaluate first operand: if true, follow with nested checks
        // This branch handles b1 == true
        if(b1 == true) {
            // First operand is true; now check second
            // Nested condition for second operand
            if(b2 == true) {
                // Both operands are true: XOR yields false
                return false;
            }
            else {
                // Exactly one operand is true (b1), so XOR yields true
                return true;
            }
        }
        else {
            // First operand is false; XOR requires second to be true
            if(b2 == true) {
                // b2 is true while b1 is false -> XOR true
                return true;
            }
            else {
                // Both operands are false: XOR yields false
                return false;
            }
        }
    }
}