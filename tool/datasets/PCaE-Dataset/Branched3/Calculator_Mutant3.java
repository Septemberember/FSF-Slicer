public class Calculator_Mutant3 {
    // Arithmetic calculator with basic operators
    // All operations are performed on two integer operands
    // Simple utility for demonstration purposes

    public static int calculate(int num1, int num2, char operator) {
        int output;
        // Determine operation based on the operator
        switch(operator) {
            case '+':
                output = num1 + num2;
                break;
            // Subtraction
            case '-':
                output = num1 - num2;
                break;
            // Multiplication (note: in this mutant, '*' uses division)
            case '*':
                output = num1 / num2; //mutated * with /
                break;
            // Division
            case '/':
                output = num1 / num2;
                break;
            // Modulus
            case '%':
                output = num1 % num2;
                break;
            default:
                // Unrecognized operator
                return -1;
        }
        return output;
    }
}