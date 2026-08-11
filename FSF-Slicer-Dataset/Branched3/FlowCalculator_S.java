public class FlowCalculator_S {

    public static double computeFlow(int pressure, int rate) {
        int adjusted = pressure;
        double flow = 0.0;
        boolean stable = true;
        int modifier = 3;

        adjusted += 7;
        adjusted *= 2;
        adjusted -= modifier;
        adjusted = adjusted + 4;

        if (adjusted > 40) {
            adjusted += 6;

            if (rate >= 5) {
                adjusted = adjusted + rate;

                if (pressure < 10) {
                    int divisor = rate - 5;
                    flow = (double) adjusted / divisor;
                } else {
                    adjusted += 8;
                    flow = adjusted * 0.95;
                    stable = false;
                }

                if (flow > 80) {
                    flow = flow * 0.9;
                } else {
                    flow = flow + 10;
                }

            } else {
                adjusted -= 4;
                flow = adjusted * 1.1;
                stable = false;
            }

        } else {
            adjusted -= 6;

            if (rate < 3) {
                adjusted += 5;
                flow = adjusted * 0.7;
            } else {
                flow = adjusted * 0.8;
                stable = false;
            }

            if (flow < 20) {
                flow = flow + 5;
            } else {
                flow = flow * 0.95;
            }
        }

        double correction = stable ? 1.1 : 0.85;
        double finalFlow = flow * correction + adjusted * 0.05;
        System.out.println("Flow result: " + finalFlow);
        return finalFlow;
    }
}
