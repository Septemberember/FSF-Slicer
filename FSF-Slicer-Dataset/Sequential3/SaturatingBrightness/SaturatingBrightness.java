public class SaturatingBrightness {
    public static int intensity(int raw) {
        int floor = Math.max(0, raw);
        int intensity = Math.min(255, floor);
        return intensity;
    }
}
