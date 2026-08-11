public class Abs_Mutant5 {
    // Abs_Mutant5: contains a simple numeric method

    // This method is intended to mimic an absolute value computation.
    // Current implementation returns -num for negative inputs and 0 otherwise.

    public static int Abs(int num) {
        // Internal condition check to illustrate control flow
        if (num < 0)
            return -num;
        else
            return 0;
    }
    // End of Abs method
}