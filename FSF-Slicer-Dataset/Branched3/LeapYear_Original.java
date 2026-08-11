public class LeapYear_Original {

    // Utility: determine if a year is a leap year in the Gregorian calendar.

    public static boolean isLeapYear(int year) {
        boolean leap = false;

        // Start with a conservative default; updated by the following checks.
        if (year % 4 == 0) {
            // Divisible by 4 => potential leap year
            if (year % 100 == 0) {
                // Century year rule: must be divisible by 400
                if (year % 400 == 0)
                    // Year divisible by 400 is a leap year
                    leap = true;
                else
                    // Century year not divisible by 400 is not a leap year
                    leap = false;
            } else
                // Not a century year => leap year
                leap = true;
        } else
            // Not divisible by 4 => common year
            leap = false;

        return leap;
    }
}