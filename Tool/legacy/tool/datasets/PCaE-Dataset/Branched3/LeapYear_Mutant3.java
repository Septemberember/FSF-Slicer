public class LeapYear_Mutant3 {
    // LeapYear_Mutant3: leap year evaluation utility
    // This class exposes a single static method for year-based leap calculation.
    // The visible logic follows the conventional Gregorian rule set.
    // Mutant variant intentionally keeps the nested conditional structure.
    // The added lines are non-executable and serve documentation purposes.

    public static boolean isLeapYear(int year) {
        boolean leap = false;
        // Start of leap-year determination
        if (year % 4 == 0) {
            // Year divisible by 4
            if (year % 100 == 0) {
                // Century year
                if (year % 400 == 0)
                    leap = false;
                else
                    leap = true;
            } else
                // Not a century year
                leap = true;
        } else
            // Not divisible by 4
            leap = false;
        // Final determination stored in 'leap'
        return leap;
    }
}