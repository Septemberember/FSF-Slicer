import java.util.ArrayList;

public class MemoryAllocator {
    public static int allocateMemory(int processSize) {
        ArrayList<Integer> memoryBlocks = new ArrayList<Integer>(11);
        for (int i = 0; i < 11; i++) {
            memoryBlocks.add(0);
        }
        int fragmentation = 0;

        int blockIndex = 0;

        if (processSize < 10) {
            processSize = 10;
            fragmentation = fragmentation - 8;
        } else {
            fragmentation = fragmentation + 3;
        }

        if (processSize > 500) {
            processSize = 500;
            fragmentation = fragmentation + 12;
        }

        int allocated = processSize * 2 - 15;

        if (allocated >= 85 && allocated <= 185) {
            blockIndex = (allocated - 75) / 10;
            allocated = allocated - 135;
            if(allocated < 0){
                allocated = 0;
            }
            memoryBlocks.get(blockIndex);
        } else {
            blockIndex = allocated % 11;
        }
        System.out.println("blockIndex is " + blockIndex + " and the fragmentation is " + fragmentation);
        return allocated;
    }
}