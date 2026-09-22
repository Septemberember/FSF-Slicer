// This class demonstrates a simple overflow-prone operation variant.
// The original intent discusses division overflow, but the current mutation uses multiplication.
// The structure remains unchanged to preserve method signatures and access.
public class DivisionOverflow_Mutant1 {
    public static int division_test_fail_overflow(int nom, int denom) {
        // Introduce a note about the operation: multiplication could overflow for large inputs.
        int tmp = nom * denom; //change division operation to multiplication
        // The result may overflow the 32-bit int range for sufficiently large nom or denom.
        return tmp;
    }
}