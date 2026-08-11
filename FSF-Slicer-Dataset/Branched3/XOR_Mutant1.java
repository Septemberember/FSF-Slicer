public class XOR_Mutant1 {

    // XOR logic method that implements a simple boolean exclusive OR
    public static boolean xor(boolean b1, boolean b2) {

        if(b1 == true) {
            return !b2;
        }
        else {
            return b2;
        }
    }

}