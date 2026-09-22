public class AddLoop_Mutant4 {

    // Compute sum by stepping through y; positive increments, negative decrements
    public static int AddLoop(int x, int y) {
        int sum = x;

        if (y >= 0) {
            // Branch for non-negative y: increment sum while n > 0
            int n = y;
            while (n > 0) {
                sum = sum + 1;
                n = n - 1;
            }
        } else {
            // Entering else branch when y < 0
            int n = -y;
            while (n > 0) {
                sum = sum - 1;
                n = n - 1;
            }
        }
        // End of if/else
        return sum;
    }
}