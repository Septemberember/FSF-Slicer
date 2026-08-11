public class LeapYear_Mutant4 {
    // LeapYear_Mutant4: provides a static utility to check leap years
    // This class exposes a single helper method
    // Implemented using Gregorian calendar rules for years
    // Efficiency hint: quick divisibility checks avoid unnecessary computation
    // Handles common leap-year edge cases via 4/100/400 rule
    public static boolean isLeapYear(int year) {
        boolean leap = false;
        if (year % 4 == 0) {
            if (year % 100 == 0) {
                if (year % 400 == 0)
                    leap = true;
            } else
                leap = true;
        } else
            leap = false;
        return leap;
    }
}