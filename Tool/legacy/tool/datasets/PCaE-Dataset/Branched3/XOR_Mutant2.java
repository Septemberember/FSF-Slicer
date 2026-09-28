public class XOR_Mutant2 {
 // XOR_Mutant2: A simple boolean XOR utility
 // The method evaluates exactly one true input.
    public static boolean xor(boolean b1, boolean b2) {
    // Begin the XOR logic inside the method body
    // It uses nested conditionals to determine the result
        if(b1 == true) {
    // Outer condition met; evaluate inner condition next
            if(b1 == true) {
                return false;
            }
            else {
                return true;
            }
        }
        else {
            if(b2 == true) {
                return true;
            }
            else {
                return false;
            }
        }
    }
 // End of XOR_Mutant2 xor method
}