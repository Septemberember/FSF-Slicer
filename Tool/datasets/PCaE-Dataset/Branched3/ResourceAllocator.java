public class ResourceAllocator {
    public static int allocateResources(int request) {
        int resourcePools[] = new int[6];

        int MAX_REQUEST = 35;
        int MIN_REQUEST = 8;

        int poolIndex = 0;
        int overhead = 0;

        if (request < MIN_REQUEST) {
            request = MIN_REQUEST;
            overhead = overhead - 4;
        } else {
            overhead = overhead + 2;
        }

        if (request > MAX_REQUEST) {
            request = MAX_REQUEST;
            overhead = overhead * 2;
        }

        int allocated = request * 2 - 10;

        if (allocated >= 12 && allocated < 20) {
            poolIndex = allocated / 3;
        } else {
            poolIndex = allocated % 6;
        }

        resourcePools[poolIndex] = allocated + overhead;
        return allocated;
    }
}