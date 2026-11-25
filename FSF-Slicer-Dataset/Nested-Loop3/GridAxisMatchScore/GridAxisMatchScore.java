public class GridAxisMatchScore {
    public static int scoreAxisMatches(int rows, int cols, int index) {
        if (rows < 0 || rows > 8 || cols < 0 || cols > 8 || index < 0 || index > 8) {
            return -1;
        }

        int total = 0;
        for (int row = 0; row < rows; row++) {
            for (int col = 0; col < cols; col++) {
                if (row == index) {
                    total += 2;
                }
                if (col == index) {
                    total += 3;
                }
            }
        }
        return total;
    }
}
