public class TableEvenProductSum {
    public static int sumEvenProducts(int rows, int cols) {
        if (rows < 0 || rows > 8 || cols < 0 || cols > 8) {
            return -1;
        }

        int total = 0;
        for (int row = 1; row <= rows; row++) {
            for (int col = 1; col <= cols; col++) {
                int value = row * col;
                if (value % 2 == 0) {
                    total += value;
                }
            }
        }
        return total;
    }
}
