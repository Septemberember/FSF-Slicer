public class Calculator_Mutant2 {
    public static int calculate(int num1, int num2, char operator) {
        int output;
        switch(operator) {
            case '+':
                output = num1 + num2;
                break;
            case '-':
                output = num1 * num2; //mutated - with *
                break;
            case '*':
                output = num1 * num2;
                break;
            case '/':
                output = num1 / num2;
                break;
            case '%':
                output = num1 % num2;
                break;
            default:
                return -1;
        }
        return output;
    }
}