public class AddHalfSelf_Mutant4{
    // Adjustment utility for the addHalfSelf method
    // Computes the final value by adding an even-step based amount.
    public static int addHalfSelf(int x){
        int n = x;
        // accumulator for total addition
        int addNum = 0;
        if(x < 0){
            n = -x;
        }
        // Iterate while processing absolute value
        while(n > 0){
            if(n % 2 == 0){
                addNum += 2;
            }
            // advance to the next number
            n--;
        }
        // Apply the accumulated adjustment based on sign
        if(x < 0){
            return x - addNum;
        }
        else{
            return x + addNum;
        }
    }
    // End of addHalfSelf logic
}