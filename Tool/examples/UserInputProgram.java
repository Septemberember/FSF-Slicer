public class UserInputProgram {
    public static int smallestCubeSumIndex(int x) {
        if (x <= 0) {
            return -1;
        }
        int sum = 0;
        int n = 0;
        while (sum < x) {
            n = n + 1;
            sum = sum + n * n * n;
        }
        return n;
    }
}

