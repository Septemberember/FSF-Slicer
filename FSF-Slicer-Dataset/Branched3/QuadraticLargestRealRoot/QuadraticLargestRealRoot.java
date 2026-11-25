public class QuadraticLargestRealRoot {
    public static double solve(int a, int b, int c) {
        if (a < -1000000000 || a > 1000000000 || b < -1000000000 || b > 1000000000 || c < -1000000000 || c > 1000000000) {
            return Double.NaN;
        }
        if (a == 0) {
            if (b == 0) {
                return Double.NaN;
            }
            return -(double)c / b;
        }
        long discriminant = (long)b * b - 4L * a * c;
        if (discriminant < 0) {
            return Double.NaN;
        }
        if (discriminant == 0) {
            return -(double)b / (2.0 * a);
        }
        double root = Math.sqrt(discriminant);
        return Math.max((-b + root) / (2.0 * a), (-b - root) / (2.0 * a));
    }
}
