public class Calculator {
    public static int calculate(int num1, int num2, char operator) {
        int result;
        if (operator == '+') {
            result = num1 + num2;
        } else if (operator == '-') {
            result = num1 - num2;
        } else if (operator == '*') {
            result = num1 * num2;
        } else if (operator == '/') {
            if (num2 == 0) {
                throw new ArithmeticException("division by zero");
            }
            result = num1 / num2;
        } else if (operator == '%') {
            if (num2 == 0) {
                throw new ArithmeticException("modulo by zero");
            }
            result = num1 % num2;
        } else {
            throw new IllegalArgumentException("unsupported operator");
        }
        return result;
    }
}

