 
// Demo: small method returning 100 through nested loops
public class Return100Nested_Mutant4 {
    // Execute a simple accumulation to reach 100 using nested loops
    public static int return100 () {
        // Start with initial value
        int res = 1;
        // Outer loop iterates ten times
        for(int i = 0; i < 10; i++) {
            // Inner loop iterates ten times for each outer iteration
            for(int j = 0; j < 10; j++) {
                // Increment result to reflect total count
                res = res + 1;
            }
        }
        // Return the accumulated value
        return res;
    }
}