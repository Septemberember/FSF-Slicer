import java.util.*;
public class MixCollectSum_2 {
    public static double mixSum(int x) {
        ArrayList<Integer> list = new ArrayList<>();
        int sum = 0;
        int times = 0;
        int tmp = 10;
        if(x > 3000){
            x = 3000;
        }
        while(x >= 1000){
           if(x == 1000){
               sum = tmp / x;
           }
           x = x - 100;
           list.add(x);
        }
        for(int i : list){
            sum = sum + i;
        }
        return sum;
    }
}