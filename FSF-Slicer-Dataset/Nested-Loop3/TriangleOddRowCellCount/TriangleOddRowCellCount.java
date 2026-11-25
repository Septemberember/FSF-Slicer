public class TriangleOddRowCellCount {
    public static int countCellsInOddRows(int size) {
        if (size < 0 || size > 12) {
            return -1;
        }

        int total = 0;
        for (int row = 1; row <= size; row++) {
            for (int col = 1; col <= row; col++) {
                if (row % 2 == 1) {
                    total++;
                }
            }
        }
        return total;
    }
}
