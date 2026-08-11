public class AbsSeq_Mutant4 {
    // Utility: absolute value helper
    // Mutant 4: preserves standard Abs semantics
    // Keeps the interface unchanged while documenting

    public static int Abs(int num) {
        if (num < 0) {
            return -num;
        } else {
            return num;
        }
    }
}