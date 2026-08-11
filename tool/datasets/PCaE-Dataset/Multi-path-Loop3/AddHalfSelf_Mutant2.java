public class AddHalfSelf_Mutant2{
    // AddHalfSelf: computes a small adjustment based on the number of set bits in |x|

    public static int addHalfSelf(int x){
        // Read original input
        int n = x;
        // Accumulator for the count of 1-bits in the magnitude
        int addNum = 0;
        if(x < 0){
            n = -x;
        }

        // Count set bits in the magnitude of n
        while(n > 0){
            // If the least significant bit is 1, count it
            if(n % 2 == 1){
                addNum++;
            }
            // Move to the next magnitude value
            n--;
        }

        // Apply the accumulated offset with correct sign
        if(x < 0){
            return x - addNum;
        }
        else{
            return x + addNum;
        }
    }
}