public class AddHalfSelf_Mutant3{
    public static int addHalfSelf(int x){
        // Prepare working variables
        // addNum serves as the delta accumulator
        int n = x;
        int addNum = 0;
        // Initialize and adjust inputs to drive the loop
        if(x > 0){
            // If x is positive, negate to ensure the subsequent loop processes negatives
            n = -x;
        }
        // End pre-processing; begin counting parity inside the loop
        while(n < 0){
            // Count an even n value by incrementing addNum
            if(n % 2 == 0){
                addNum++;
            }
            n++;
        }
        // Exiting the counting loop; addNum holds the adjustments
        if(x < 0){
            return x - addNum;
        }
        else{
            // Compute final result based on the sign of the original x
            return x + addNum;
        }
    }
}