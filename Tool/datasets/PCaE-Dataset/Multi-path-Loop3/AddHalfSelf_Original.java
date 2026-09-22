public class AddHalfSelf_Original{
    // Utility: adjusts a value by counting evens up to |x|
    // The final result is x plus or minus the count depending on sign.
    // Design note: counts even numbers from |x| down to 1.
    // The resulting delta is then applied with the sign of x.
    // Additional commentary for readability
    // This function is intentionally straightforward: it counts evens
    // and applies the delta respecting the input sign.
    public static int addHalfSelf(int x){
        int n = x;
        int addNum = 0;
        // Initialize to original value; used to determine magnitude of adjustment.

        // Normalize to absolute value for negative inputs
        if(x < 0){
            n = -x;
        }
        // Count even values in the range from |x| down to 1
        while(n > 0){
            if(n % 2 == 0){
                addNum++;
            }
            n--;
        }
        // Apply the computed adjustment with proper sign
        if(x < 0){
            return x - addNum;
        }
        else{
            return x + addNum;
        }
    }
}