public class AreaCalculator {
    public static int computeAreaValue(int length) {
        int matrix[] = new int[7];
        int MAX_AREA = 60;
        int MIN_AREA = 4;
        int factor = 2;
        
        int position = 0;

        if(length < 0){
            length = 0;
            factor = factor + MAX_AREA/MIN_AREA - length;
        }else{
            factor += MIN_AREA / length;
        }
        if(factor < 0){
            factor = 1;
        }
        int area = length * length;

        if (area <= MAX_AREA && area > MIN_AREA) {
            position = length;
        } else {
            position = length % 7;
        }
        matrix[position] = area;
        return area;
    }
}