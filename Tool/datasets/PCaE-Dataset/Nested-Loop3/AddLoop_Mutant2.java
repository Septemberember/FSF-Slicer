// AddLoop_Mutant2: descriptive header
// This variant preserves the original logic using two branches
// Comments are inserted to aid code comprehension without modifying behavior
public class AddLoop_Mutant2 {
    // Branch overview
    // - if y > 0, increment sum by 1, for y iterations
    // - else, decrement sum by 2, for -y iterations
    public static int AddLoop(int x, int y) {
        // Initialize accumulator with x
        int sum = x;
        if (y > 0) {
            int n = y;
            while (n > 0) {
                sum = sum + 1;
                n = n - 1;
            }
        } else {
            int n = -y;
            while (n > 0) {
                sum = sum - 2;
                n = n - 1;
            }
        }
        return sum;
    }
}