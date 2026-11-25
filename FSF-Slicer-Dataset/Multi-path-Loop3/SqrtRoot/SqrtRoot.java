// Source: adapted implementation and specifications from the independent 236-program maintenance corpus, Multi-path Loop/SqrtRoot/SqrtRoot.verified.java.
public class SqrtRoot {

    public static int sqrtRoot(int num) {
        if (num < 0) {
            return -1;
        }
        int left = 0;
        int right = num;

        while (left <= right) {
            int mid = left + (right - left) / 2;

            if ((long) mid * mid == num) {
                return mid;
            } else if ((long) mid * mid < num) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        return right;
    }
}
