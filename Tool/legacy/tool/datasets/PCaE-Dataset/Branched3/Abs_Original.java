public class Abs_Original {

    // Abs_Original: simple utility to compute absolute value of an int.
    // The implementation uses a straightforward conditional check.

    public static int Abs(int num) {
        if (num < 0)
            return -num;
        else
            return num;
    }
}