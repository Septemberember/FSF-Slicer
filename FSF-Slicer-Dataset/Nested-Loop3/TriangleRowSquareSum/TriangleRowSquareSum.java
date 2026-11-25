public class TriangleRowSquareSum {
    public static int sumRowSquares(int size) {
        if (size < 0 || size > 12) {
            return -1;
        }

        int total = 0;
        for (int row = 1; row <= size; row++) {
            for (int col = 1; col <= row; col++) {
                total += row;
            }
        }
        return total;
    }
}
