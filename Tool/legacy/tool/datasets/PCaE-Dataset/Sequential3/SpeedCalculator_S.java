public class SpeedCalculator_S {
    public static int calculateSpeed(int time) {
        int buffer[] = new int[6];
        int MAX_TIME = 50;
        int MIN_TIME = 5;
        
        int offset = 0;
        int adjustment = 0;

        if (time < MIN_TIME) {
            time = MIN_TIME;
            adjustment = adjustment - 10;
        } else {
            adjustment = adjustment + 5;
        }

        if (time > MAX_TIME) {
            time = MAX_TIME;
            adjustment = adjustment * 2;
        }

        int speed = 100 - time * 2;

        if (speed >= 10 && speed < 24) {
            offset = speed / 4;
        } else {
            offset = speed % 6;
        }
        
        buffer[offset] = speed + adjustment;
        return speed;
    }
}