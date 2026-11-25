public class DivisionOverflow_Mutant2 {
    public static int division_test_fail_overflow(int nom, int denom) {
        int tmp = nom / (denom+1); // modifying denom by adding 1
        return tmp;
    }
}