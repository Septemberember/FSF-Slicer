public class EuclideanRemainderGcd {
    public static int gcd(int a, int b) {
        if (a < -1024 || a > 1024 || b < -1024 || b > 1024) {
            return -1;
        }
        a = Math.abs(a);
        b = Math.abs(b);
        while (b != 0) {
            int remainder = a;
            while (remainder >= b) {
                remainder -= b;
            }
            a = b;
            b = remainder;
        }
        return a;
    }
}
