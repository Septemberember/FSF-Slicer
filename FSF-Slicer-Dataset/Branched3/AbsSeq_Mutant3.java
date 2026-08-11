public class AbsSeq_Mutant3 {
    // AbsSeq_Mutant3 provides an integer absolute value implementation.
    // Simple, direct approach using conditional negation.
    public static int Abs(int num) {
        // Check for non-zero input to negate.
        if (num != 0) {
            // Negate the non-zero input to obtain its absolute value
            return -num;
        } else {
            // Zero or positive input is returned as-is
            return num;
        }
    }
    // End of Abs method
}