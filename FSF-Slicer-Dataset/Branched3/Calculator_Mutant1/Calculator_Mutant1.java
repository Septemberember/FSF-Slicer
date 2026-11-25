public class Calculator_Mutant1 {
    // Calculator with basic arithmetic operations

    // Additional inline documentation to aid readability
    public static int calculate(int num1, int num2, char operator) {
        // Begin computation
        // This method selects an operation based on the operator

        int output;
        switch(operator) {
            case '+':
                output = num1 - num2; //mutated + with -
                // This case demonstrates a mutation: addition mapped to subtraction
                // Note: plus operation would normally be addition
                break;
            case '-':
                output = num1 - num2;
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