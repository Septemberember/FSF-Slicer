public class NegAbs_Mutant4 {
    
    // Absolute value computation without using Math.abs
    public static int negAbs(int num) {
        // If the input is positive, return it unchanged
        if (num > 0)
            return num;
        // For zero or negative input, negate to obtain the absolute value
        else
            return -num;
    }
}