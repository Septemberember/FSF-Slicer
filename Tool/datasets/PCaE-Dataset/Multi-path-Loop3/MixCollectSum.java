import java.util.*;
public class MixCollectSum {
    public static double mixSum(int x) {
        ArrayList<Integer> list = new ArrayList<>();
        int sum = 0;
        int times = 0;
        int tmp = 10;
        if(x > 220){
            x = 220;
        }
        while(x >= 195){
           if(x == 200){
               x = x - 150;
               sum = tmp / x;
           }
           x = x - 1;
           list.add(x);
        }
        for(int i : list){
            sum = sum + i;
        }
        return sum;
    }
}