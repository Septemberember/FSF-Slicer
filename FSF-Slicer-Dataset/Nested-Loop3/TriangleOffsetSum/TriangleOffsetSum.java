public class TriangleOffsetSum {
    public static int sumColumnOffsets(int size) {
        if (size < 0 || size > 12) {
            return -1;
        }

        int total = 0;
        for (int row = 1; row <= size; row++) {
            for (int col = 1; col <= row; col++) {
                total += row - col;
            }
        }
        return total;
    }
}
