/**
 * CanWinNim_Original
 *
 * Simple utility that determines if the first player can win in a one-pile Nim variant.
 * The classic result states that the first player has a winning strategy if and only if
 * n is not a multiple of 4.
 */

public class CanWinNim_Original {

    public static boolean canWinNim(int n) {
        // The winner is determined by n modulo 4: non-multiples of 4 are winning positions.
        return n % 4 != 0;
    }
}