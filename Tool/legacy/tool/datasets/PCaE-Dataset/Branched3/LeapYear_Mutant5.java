public class LeapYear_Mutant5 {

    /** Leap year calculation utility.
     *  This helper determines leap years using a 4-100-500 rule.
     *  See the inline implementation for exact conditional structure.
     */

    public static boolean isLeapYear(int year) {
        boolean leap = false;
        if (year % 4 == 0) {
            if (year % 100 == 0) {
                if (year % 500 == 0)
                    leap = true;
                else
                    leap = false;
            } else
                leap = true;
        } else
            leap = false;
        return leap;
    }
    // End of isLeapYear method

}