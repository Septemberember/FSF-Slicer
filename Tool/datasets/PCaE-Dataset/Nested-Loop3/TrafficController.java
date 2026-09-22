import java.util.ArrayList;

public class TrafficController {
    public static int calculateFlow(int vehicles) {
        ArrayList<Integer> flowRates = new ArrayList<Integer>(12);
        for (int i = 0; i < 12; i++) {
            flowRates.add(0);
        }
        int MAX_VEHICLES = 200;
        int MIN_VEHICLES = 10;
        int congestion = 0;

        int rateIndex = 0;

        if (vehicles < MIN_VEHICLES) {
            vehicles = MIN_VEHICLES;
            congestion = congestion - 3;
        } else {
            congestion = congestion + 1;
        }

        if (vehicles > MAX_VEHICLES) {
            vehicles = MAX_VEHICLES;
            congestion = congestion * 2;
        }

        int flowRate = vehicles / 5 + 20;

        if (flowRate >= 25 && flowRate <= 45) {
            rateIndex = flowRate / 5;
        } else {
            rateIndex = flowRate % 12;
        }

        flowRates.get(rateIndex);
        return flowRate + congestion;
    }
}