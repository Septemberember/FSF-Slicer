public class XOR_Mutant5 {
    // Entry point of XOR operation
    public static boolean xor(boolean b1, boolean b2) {
        // Evaluate first input
        if(b1 == true) {
            // First input is true
            if(b2 == true) {
                // Both inputs are true -> result is false
                return false;
            }
            else {
                // Only first input is true
                return b1;
            }
        }
        else {
            // First input is false
            if(b2 == true) {
                // Only second input is true
                return b1;
            }
            else {
                // Both inputs are false
                return false;
            }
        }
    }
}