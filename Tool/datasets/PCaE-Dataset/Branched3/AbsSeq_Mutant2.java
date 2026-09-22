public class AbsSeq_Mutant2 {
    // AbsSeq_Mutant2: helper for absolute value computation

    public static int Abs(int num) {
        // Compute absolute value: negate when negative
        if (num < 0) {
            // Flip sign for negative values
            return num * -1;
        } else {
            // Positive or zero remains unchanged
            return num;
        }
    }
}