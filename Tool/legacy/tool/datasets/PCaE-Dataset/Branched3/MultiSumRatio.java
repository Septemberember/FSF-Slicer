public class MultiSumRatio {
    public static int multiSumRatio(int x, int y) {
        int sum = x;
        int ratio = 0;
        int factor = 1;
        if(y < 0){
            y = -y;
        }
        if (y > 0) {
            int n = y;
            while (n > 0) {
                sum = sum + 1;
                n = n - 1;
                factor += n;
            }
        } else {
            int n = -y;
            while (n > 0) {
                sum = sum - 1;
                n = n - 1;
                factor += n;
            }
        }
        int tmpFactor = 0;
        while(factor > 10){
            tmpFactor++;
            factor /= 10;
        }
        int multi = x * y;
        ratio = multi / sum;
        ratio = ratio * tmpFactor;
        return ratio;
    }
}