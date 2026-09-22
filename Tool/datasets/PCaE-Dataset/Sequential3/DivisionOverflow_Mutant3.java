/* 
 * DivisionOverflow_Mutant3
 * This mutant demonstrates a straightforward division operation
 * after incrementing the numerator, with commentary added.
 * No changes to the executable code are made.
 */
 
public class DivisionOverflow_Mutant3 {
    // Prepare the inputs for division to simulate a simple edge case.
    public static int division_test_fail_overflow(int nom, int denom) {
        // Increment the numerator before division; behavior is unchanged otherwise.
        int tmp = (nom+1) / denom; // modifying nom by adding 1
        // Return the computed quotient for potential downstream validation.
        return tmp;
    }
}