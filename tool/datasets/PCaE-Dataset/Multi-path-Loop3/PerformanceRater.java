public class PerformanceRater {
    public static double calculateBonus(int sales) {
        int attendance = 64;
        int bonusLevels[] = new int[4];
        int factor = 0;
        String performance = null;
        bonusLevels[0] = 100;
        bonusLevels[1] = 300;
        bonusLevels[2] = 500;
        bonusLevels[3] = 800;

        int baseSalary = 2000;
        int penalty = 0;
        int rating = 0;

        if(sales > baseSalary * 10){
            return sales + baseSalary * 10;
        }

        if (sales < 0 || sales < 120) {
            return baseSalary;
        }

        if (sales > 10000) {
            return baseSalary + bonusLevels[3] + (sales - 10000) / 100;
        }

        rating = sales / 125;

        performance = new String(String.valueOf(rating * 2) + 9);

        if (attendance < 80) {
            penalty = (100 - attendance) * 10;
        }
        int bonus = 0;
        if (rating == 0) {
            bonus = bonusLevels[0] - penalty;
            bonus =  Math.max(bonus, 0);
            performance = null;
            System.out.println("bonus is " + bonus);
        }
        if (rating == 1) {
            bonus = bonusLevels[1] - penalty / 2;
            bonus =  bonus + (sales % 100);
            System.out.println("bonus is " + bonus);
        }
        if (rating == 2) {
            bonus = bonusLevels[2] - penalty / 3;
            bonus = bonus + (attendance * 2);
            System.out.println("bonus is " + bonus);
        } else {
            bonus = sales * bonusLevels[3] / 1000;
            if (bonus > 1000) {
                bonus = bonus + attendance * 5;
            }
            System.out.println("bonus is " + bonus);
        }
        factor = performance.length();

        return (baseSalary + bonus) * (double)(factor / 2);
    }
}