public class TriangleBoundaryCellCount {
    public static int countBoundaryCells(int size) {
        if (size < 0 || size > 12) {
            return -1;
        }

        int total = 0;
        for (int row = 1; row <= size; row++) {
            for (int col = 1; col <= row; col++) {
                if (row == size || col == 1 || col == row) {
                    total++;
                }
            }
        }
        return total;
    }
}
