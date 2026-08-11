public class TaxCalculator {
    public static int calculateTax(int income) {
        int taxBrackets[] = new int[5];
        taxBrackets[0] = 0;
        taxBrackets[1] = 1;
        taxBrackets[2] = 2;
        taxBrackets[3] = 3;
        taxBrackets[4] = 4;

        int deduction = 1000;
        int tax = 0;
        int level = 0;
        
        if(income < 0) {
            return 0;
        }
        if(income > 16000){
            return income / 2;
        }
        
        int taxableIncome = income - deduction;
        if(taxableIncome <= 0) {
            return 0;
        }
        
        level = taxableIncome / 3000;
        if(level < 0) {
            level = 0;
        }
        
        if(level == 0) {
            tax = taxableIncome * taxBrackets[1] / 10;
            if(tax < 100){
                tax = 0;
            } else {
                tax = tax - 100;
            }

        }
        if(level == 1) {
            tax = (taxableIncome - 3000) * taxBrackets[2] / 10 + 300;
            tax = tax + (taxableIncome % 500);
        }
        if(level == 2) {
            tax = (taxableIncome - 6000) * taxBrackets[3] / 10 + 900;
            tax = tax - (tax % 200);
        } else {
            tax = taxableIncome * taxBrackets[level] / 10;
            if(tax > 5000) {
                tax = tax + taxBrackets[4] * 10;
            }
        }
        tax = tax < 0 ? 0 : tax;
        return tax;
    }
}