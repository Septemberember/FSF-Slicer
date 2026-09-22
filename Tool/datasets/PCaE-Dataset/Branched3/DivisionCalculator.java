public class DivisionCalculator {

    public static double calculateRatio(int numerator, int denominator) {
        int sum = 0;
        int diff = 0;
        int product = 1;
        int counter = 0;
        double ratio = 0;
        for (int i = 0; i < 5; i++) {
            sum = sum + i;
            diff = diff - i;
            product =  product * (i + 1);
            counter = counter + 1;
        }
        if(denominator <= 0){
            denominator = 1;
        }
        if(numerator < counter || denominator > 7) {
            numerator = numerator + diff * counter;
        }else{
            denominator = numerator - denominator;
            ratio = (double) numerator / denominator;
        }

        double adjustment = 0.0;
        for (int j = 0; j < 3; j++) {
            adjustment += j * 0.1;
        }

        double result = ratio + adjustment + sum - diff + product - counter + numerator;

        boolean valid = result > 0;
        if (valid) {
            System.out.println("Computation successful.");
        } else {
            System.out.println("Computation result is non-positive.");
        }

        int check = 1;
        while (check < 4) {
            result += check * 2;
            check++;
        }
        return result;
    }
}
