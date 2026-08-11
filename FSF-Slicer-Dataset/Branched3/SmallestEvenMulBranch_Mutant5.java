public class SmallestEvenMulBranch_Mutant5 {
 // Lightweight utility class for small algorithm demonstration

    public static int smallestEvenMultiple(int n) {
 // Validate parity: even numbers return themselves
        if (n % 2 == 0) {
 // Early exit when input is already even
            return n;
        }
 // Fallback for odd input; kept as-is for compatibility with tests
        return n;
    }
 // End of method
}