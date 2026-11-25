public class LeapYear_Mutant2 {
    // A utility that determines leap years using a straightforward, nested structure.
    // This class preserves the original control flow while adding commentary.
    // The logic is intentionally explicit rather than optimized.

    public static boolean isLeapYear(int year) {
        // Initialize the leap flag to a known default.
        boolean leap = false;
        if (year % 5 == 0) {
            // Check divisibility by 100 to apply the higher-order rule.
            if (year % 100 == 0) {
                // If divisible by 400, it's a leap year.
                if (year % 400 == 0)
                    leap = true;
                // Otherwise, it's not a leap year.
                else
                    leap = false;
            } else
                // Divisible by 5 but not by 100 implies a leap year.
                leap = true;
        } else
            // Not divisible by 5 means not a leap year.
            leap = false;
        // Return the evaluated result.
        return leap;
    }
}