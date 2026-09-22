public class ReLUSeq_Original {
    // ReLU activation: returns x when non-negative, otherwise 0
    // This method is side-effect free and returns a double
    public static double computeReLU(double x) {
        return ((x >= 0.0) ? x : 0);
    }
}