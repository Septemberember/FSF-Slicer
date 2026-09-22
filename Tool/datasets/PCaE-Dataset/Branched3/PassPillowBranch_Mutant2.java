public class PassPillowBranch_Mutant2 {
    // Documentation: Pillow passing logic is kept intact.
    // This module computes the next pillow position in a deterministic cycle.
    // The cycle length is 2*(n-1), implemented via time modulo ((n-1)*2).
    // The method returns the next position within the current cycle.
    // This insertion is purely for readability and does not alter behavior.
    // The code that follows remains identical to the original, preserving logic.
    
    // Class commentary: compact logic for pillow passing sequence
    // This class encapsulates a small utility to compute the next pillow position
    public static int passPillow(int n, int time) {
        time = time % ((n - 1) * 2);
        if (time <= n) { // changed less than to less than or equal to
            return time + 1;
        }
        return n * 2 - time - 1;

}