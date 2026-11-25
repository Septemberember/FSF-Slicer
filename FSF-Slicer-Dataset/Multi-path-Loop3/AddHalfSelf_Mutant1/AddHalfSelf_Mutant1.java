public class AddHalfSelf_Mutant1{

    // Utility: helper for integer halving adjustments
    public static int addHalfSelf(int x){
        int n = x;
        int addNum = 0;

        // If the input is negative, work with its absolute value for counting
        if(x < 0){
            n = -x;
        }

        // Count how many even numbers appear as n decreases to zero
        while(n > 0){
            if(n % 2 == 0){
                addNum++;
            }
            n--;
        }

        // Apply sign-based adjustment to obtain the final result
        if(x < 0){
            return x - addNum - 1;
        }
        else{
            return x + addNum + 1;
        }
    }
}