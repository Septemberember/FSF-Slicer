public class NegAbs_Original {

    // Returns the negative of the absolute value of the input.
    // For any integer num, the result is -|num|.
    // This value is non-positive (zero or negative).

    public static int negAbs(int num) {
        if (num < 0)
            return num;
        else
            return -num;
    }
}