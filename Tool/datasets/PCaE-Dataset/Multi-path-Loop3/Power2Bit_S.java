public class Power2Bit {
    public static int power2Bit(int n) {
        int x = 2;
        int MAX_LENGTH = 8;
        int MKS = 88;
        int base = 0;
        int res = 1;
        String s = null;
        if(n < 0){
            n = -n;
        }
        if(n >= 0){
            if(n < 6){
                for(int i = 0; i <= n; i++){
                    res = res * x;
                    String resStr = new String(String.valueOf(res));
                    s = resStr;
                    if(i == 3 && res > MKS){
                        base = 2;
                    }
                }
            }else{
                res = MAX_LENGTH;
                String resStr = new String(String.valueOf(res));
                s = resStr;
                base = 1;
            }
        }
        res = s.length();
        return res + base;
    }
}