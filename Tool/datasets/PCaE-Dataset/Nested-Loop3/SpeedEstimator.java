public class SpeedEstimator {

    public static double estimateSpeed(int distance,int time) {
        int adjusted = distance;
        double speed = 0.0;
        boolean valid = true;
        int bias = 2;

        adjusted += 10;
        adjusted *= 2;
        adjusted -= bias;
        adjusted = adjusted + 5;

        if (adjusted > -50 && adjusted <= 67) {
            adjusted += 4;
            if (time < 5) {
                adjusted = adjusted + time * 2;

                if (distance > 20) {
                    adjusted = adjusted + distance - 4;
                    speed = adjusted * 0.75;
                    adjusted -= 5;

                    if (time > 0) {
                        adjusted += 2;

                        if (time != 0) {
                            int divisor = time - 1;
                            speed = (double) adjusted / divisor;
                        } else {
                            adjusted += 4;
                            speed = adjusted * 1.05;
                            valid = false;
                        }

                    } else {
                        adjusted += 3;
                        speed = adjusted * 0.6;
                    }
                } else {
                    adjusted += 3;
                    speed = adjusted * 1.1;
                    valid = false;
                }

            } else {
                adjusted -= 6;
                speed = adjusted * 0.8;
                valid = false;
            }

        }
        double factor = valid ? 1.1 : 0.85;
        double finalSpeed = speed * factor + adjusted * 0.04;
        System.out.println("Speed result: " + finalSpeed);
        return finalSpeed;
    }
}
