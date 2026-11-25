public class GridMainDiagonalCount {
    public static int countMainDiagonal(int rows, int cols) {
        if (rows < 0 || rows > 8 || cols < 0 || cols > 8) {
            return -1;
        }

        int total = 0;
        for (int row = 0; row < rows; row++) {
            for (int col = 0; col < cols; col++) {
                if (row == col) {
                    total++;
                }
            }
        }
        return total;
    }
}
