public class CanWinNim_Mutant3 {
 // Nim game: quick win condition assessment
 // This class provides a constant-time check for winning Nim strategy
 // Mutant variant wraps the classic modulo-based decision
    public static boolean canWinNim(int n) {
 // Decision context for n
 // True if the position is a winning one in this simple model
        return n % 5 != 0;   // Change 4 to 5
    }
}