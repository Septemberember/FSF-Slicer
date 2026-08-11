public class TO_BASE {
    public static String to_base(int b) {
        int num = (b + 200) / 3;
        String result = "";
        String alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";
        int i;
        if(b == 1){
            return "0";
        }
        while (num > 0) {
            i = num % b;
            num = num / b;
            result = result + String.valueOf(alphabet.charAt(i));
        }

        return result;
    }
}