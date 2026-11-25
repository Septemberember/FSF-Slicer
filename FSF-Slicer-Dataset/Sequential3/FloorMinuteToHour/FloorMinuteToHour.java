public class FloorMinuteToHour {
    public static int hourOfDay(int minute) {
        int offset = minute % 1440;
        int normalized = (offset + 1440) % 1440;
        return normalized / 60;
    }
}
