import java.util.ArrayList;

public class ProductionScheduler {
    public static int calculateOutput(int hours) {
        ArrayList<Integer> productionSlots = new ArrayList<Integer>(8);
        for (int i = 0; i < 8; i++) {
            productionSlots.add(0);
        }
        int cal = 0;
        int MAX_HOURS = 24;
        int MIN_HOURS = 4;
        int efficiency = 0;

        int slotIndex = 0;

        if (hours < MIN_HOURS) {
            hours = MIN_HOURS;
            efficiency = efficiency - 2;
        } else {
            efficiency = efficiency + 1;
        }

        if (hours > MAX_HOURS) {
            hours = MAX_HOURS;
            efficiency = efficiency + 3;
        }

        int output = hours * 30 + 50;

        if (output >= 200 && output <= 350) {
            slotIndex = output / 50;
        } else {
            slotIndex = output % 8;
        }

        cal = productionSlots.get(slotIndex);

        if(cal * efficiency > MAX_HOURS) {
            output = output + efficiency * 2;
        } else {
            output = output - efficiency;
        }

        return output;
    }
}