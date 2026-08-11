public class PaymentProcessor {
    public static String calculateChange(int payment) {
        int MAX_PAYMENT = 100;
        int MIN_PAYMENT = 20;

        int slot = 0;
        int fee = 0;

        if (payment < MIN_PAYMENT) {
            payment = MIN_PAYMENT;
            fee = fee - 5;
        } else {
            fee = fee + 3;
        }

        if (payment > MAX_PAYMENT) {
            payment = MAX_PAYMENT;
            fee = fee * 2;
        }

        int change = payment - 15;
        String bill = null;

        if (change >= 8 && change <= 16) {
            slot = change / 2;
        } else {
            slot = change % 8;
        }

        if(slot > 0 && slot < 8){
            bill = new String(String.valueOf(change + fee));
        }
        if(bill.length() > 10){
            bill = bill.substring(0, 10);
        }
        return bill;
    }
}