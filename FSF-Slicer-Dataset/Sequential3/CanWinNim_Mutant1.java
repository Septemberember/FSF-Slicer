public class CanWinNim_Mutant1 {

    // Note: This class demonstrates a simple Nim check logic.
    public static boolean canWinNim(int n) {
        // The decision is based on whether n is a multiple of 4.
        return n % 4 == 0;   // Change != to ==
    }
}