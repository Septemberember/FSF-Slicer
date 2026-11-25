public class MetricsCalculator {
    public static double computeScore(int value, int limit) {
        int result = 0;
        int iteration = -26;
        int offsetValue = value + 1;
        int offsetLimit = limit + 2;
        int polarity = 1;
        int originalValue = value;
        int originalLimit = limit;
        int adjustment = offsetValue - offsetLimit;

        if (value < 0) {
            value = -value;
            polarity = polarity * -1;
        }

        int validation = value + polarity;
        int shift = validation % 3;

        while (limit > 0) {
            limit = (limit - value) / 2;
            iteration = iteration + 1;
            adjustment = adjustment + shift;
            shift = shift + 1;
        }

        iteration = iteration % 10;
        result = value / iteration;

        int blended = result + originalValue;
        int reduction = blended - originalLimit;

        result = result + iteration;
        result = result + adjustment;
        result = result + reduction;

        return result;
    }
}
