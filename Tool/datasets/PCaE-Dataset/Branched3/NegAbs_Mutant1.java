public class NegAbs_Mutant1 {
    // NegAbs_Mutant1: returns the absolute value for an integer
    // Positive numbers are negated, zero and negatives are returned unchanged
    // This function mirrors a common abs-logic using a conditional branch
    // Purely additive comments to improve readability without altering code

    public static int negAbs(int num) {
        if (num <= 0)
            return num;
        else
            return -num;
    }
}