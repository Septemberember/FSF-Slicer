public class BoundedCubeSumIndex {
    public static int smallestCubeSumIndex(int x) {
        if (x <= 0 || x > 784) {
            return -1;
        }
        int sum = 0;
        int n = 0;
        while (sum < x) {
            n++;
            sum += n * n * n;
        }
        return n;
    }
}
