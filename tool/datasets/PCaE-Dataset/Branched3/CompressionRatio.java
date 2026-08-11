public class CompressionRatio {
    public static String calculateRatio(int fileSize) {
        String ratioStr = null;
        int level = 0;
        int overhead = 0;

        if (fileSize < 50) {
            fileSize = 50;
            overhead = overhead - 3;
            overhead *= fileSize / 10;
        } else {
            overhead = overhead + 1;
            overhead *= fileSize / 100;
        }

        if (fileSize > 400) {
            fileSize = 400;
            overhead = overhead + 5;
            overhead *= fileSize / 100;
        }

        if(overhead > 80){
            overhead = overhead > 100 ? 100 : overhead;
            overhead = overhead / 10;
        }else{
            overhead = overhead < 10 ? 10 : overhead;
            overhead = overhead / 10;
        }

        int ratio = fileSize / 4 + 30;

        if (ratio >= 45 && ratio <= 70) {
            level = (ratio - 45) / 5;
            if(level < 5) {
                ratioStr = new String("ratio:" + ratio);
            }
        } else {
            level = 5 + (ratio % 5);
            ratioStr = new String("ratio:" + ratio);
        }
        ratioStr.trim();
        ratioStr = ratioStr + " level:" + level + " overhead:" + overhead;
        return ratioStr;
    }
}