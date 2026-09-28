public class CanWinNim_Mutant2 {
    
    // Nim game insight: determine if the first player can force a win
    // for a pile of n stones using optimal play.
    // The well-known rule is that the first player wins if n % 3 != 0.
    // The method below preserves the original logic while providing clarifying notes.
    public static boolean canWinNim(int n) {
        return n % 3 != 0;   // Change 4 to 3
    }
    // End of canWinNim helper
}