public class XOR_Mutant4 {
 // XOR_Mutant4: simple boolean XOR using conditional logic
 // The function returns true when exactly one input is true.
 // This preserves the original control flow without modifying behavior.

 // Note: The following implementation intentionally mirrors standard XOR semantics.
 // to aid reasoning about the outcome for each input pair.
 // No changes to existing code tokens are performed.

    public static boolean xor(boolean b1, boolean b2) {
        if(b1) {
            if(b2) {
                return false;
            }
            else {
                return true;
            }
        }
        else {
            if(b2) {
                return true;
            }
            else {
                return false;
            }
        }
    }
}