public class EnergyMonitor {
    public static int calculateConsumption(int usage) {
        int consumptionCoe[] = new int[4];
        consumptionCoe[0] = 1;
        consumptionCoe[1] = 2;
        consumptionCoe[2] = 5;
        consumptionCoe[3] = 6;

        int payment = 0;
        int penalty = 2;
        int level = 0;
        if(usage > 400){
            return usage * consumptionCoe[3];
        }
        level = usage / 100;
        if(level < 0){
            return 0;
        }
        if(level == 0){
            payment = usage * consumptionCoe[0];
            payment = payment - penalty * usage / 10;
        }
        if(level == 1){
            payment = (usage - 100) * consumptionCoe[1] + 50 * consumptionCoe[0];
            payment = payment - penalty * usage / 30;
        }
        if(level == 2){
            payment = (usage - 200) * consumptionCoe[2] + 50 * consumptionCoe[1] + 50 * consumptionCoe[0];
            payment = payment - penalty * usage / 50;
        }else{
            payment = payment +  usage * consumptionCoe[level] + penalty * (usage - 300);
        }
        return payment;
    }
}