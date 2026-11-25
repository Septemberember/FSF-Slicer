public class GridColumnPrefixSum {
    public static int sumPrefixColumns(int rows, int cols, int width) {
        if (rows < 0 || rows > 8 || cols < 0 || cols > 8 || width < 0 || width > 8) {
            return -1;
        }

        int total = 0;
        for (int row = 1; row <= rows; row++) {
            for (int col = 1; col <= cols; col++) {
                if (col <= width) {
                    total += col;
                }
            }
        }
        return total;
    }
}
