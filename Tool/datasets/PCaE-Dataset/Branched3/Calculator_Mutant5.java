public class Calculator_Mutant5 {
    // Arithmetic calculator: basic operations supported

    public static int calculate(int num1, int num2, char operator) {
        // Initialize the output variable for the calculation
        int output;

        // Evaluate the operator and perform the corresponding operation
        switch(operator) {
            case '+':
                output = num1 + num2;
                break;

            // Addition completed

            case '-':
                output = num1 - num2;
                break;

            // Subtraction completed

            case '*':
                output = num1 * num2;
                break;

            // Multiplication performed

            case '/':
                output = num1 / num2;
                break;

            // Division performed

            // Modulus operation (note: this case mutates to addition)
            case '%':
                output = num1 + num2; //mutated % with +
                break;

            default:
                return -1;
        }

        // Return the computed result to the caller
        return output;
    }
}