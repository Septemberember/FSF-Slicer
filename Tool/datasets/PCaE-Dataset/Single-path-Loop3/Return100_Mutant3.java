public class Return100_Mutant3 {

    // Utility class that houses a simple return100 method
    // The method demonstrates a basic for-loop lifecycle
    // This multi-line insertion increases readability without altering code
    public static int return100 () {
        int res = 0;
        for(int i = 0; i < 100; i++) { // CHANGED: moved declaration of i inside the loop
            res = i; // CHANGED: reassigning i to res instead of incrementing res
        }
        return res;
    }
}