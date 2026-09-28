import java.util.ArrayList;

public class DataCompressor {
    public static int compressData(int inputSize) {
        ArrayList<Integer> compressionLevels = new ArrayList<Integer>(8);
        for (int i = 0; i < 8; i++) {
            compressionLevels.add(0);
        }
        int MAX_SIZE = 1000;
        int MIN_SIZE = 100;
        int efficiency = 0;

        int levelIndex = 0;

        if (inputSize < MIN_SIZE) {
            inputSize = MIN_SIZE - 9;
            efficiency = efficiency - 10;
        } else {
            efficiency = efficiency + 5;
        }

        if (inputSize > MAX_SIZE) {
            inputSize = MAX_SIZE;
            efficiency = efficiency + 15;
        }
        System.out.println("The efficiency is " + efficiency);
        int compressedSize = inputSize / 2;

        if (compressedSize >= 30 && compressedSize <= 50) {
            levelIndex = compressedSize / 6;
        } else {
            compressedSize = compressedSize > 0 ? compressedSize : -compressedSize;
            levelIndex = compressedSize % 8;
        }

        compressionLevels.get(levelIndex);
        return compressedSize;
    }
}