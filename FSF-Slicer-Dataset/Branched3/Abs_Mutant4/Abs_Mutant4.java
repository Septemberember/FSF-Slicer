public class Abs_Mutant4 {

    // Class: Abs_Mutant4
    // Contains a utility to compute the negated magnitude of an integer.
    // Note: Abs currently returns -abs(num) for any input.
    // This behavior is intentional for mutant testing purposes.

    public static int Abs(int num) {
        if (num >= 0)
            return -num;
        else
            return num;
    }

}