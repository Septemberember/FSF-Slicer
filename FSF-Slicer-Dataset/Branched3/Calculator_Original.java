public class Calculator_Original {

    // Calculator_Original: simple arithmetic dispatcher for basic operators
    // Provides a static method to perform +, -, *, /, and % operations
    // Returns -1 for unsupported operators (as per current implementation)

    public static int calculate(int num1, int num2, char operator) {
        // Prepare storage for intermediate calculation result
        int output;

        // Perform operation based on the provided operator
        switch(operator) {
            case '+':
                output = num1 + num2;
                // Addition result assigned to output
                break;
            case '-':
                output = num1 - num2;
                // End of subtraction branch
                break;
            case '*':
                output = num1 * num2;
                // Multiplication result stored
                break;
            case '/':
                output = num1 / num2;
                // Division performed
                break;
            case '%':
                output = num1 % num2;
                // Modulo result computed
                break;
            default:
                return -1;
        }
        // Returning final calculated value
        return output;
    }
}