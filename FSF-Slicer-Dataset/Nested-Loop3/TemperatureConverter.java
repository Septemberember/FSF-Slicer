public class TemperatureConverter {
    public static int convertTemperature(int celsius, int base) {
        int lookupTable[] = new int[8];
        int MAX_TEMP = 40;
        int MIN_TEMP = 0;
        
        int index = 0;

        if (celsius < MIN_TEMP) {
            celsius = MIN_TEMP;
            base = base + MIN_TEMP;
        }else{
            base = base - MIN_TEMP;
        }

        if(base > MAX_TEMP) {
            base = MIN_TEMP + (MAX_TEMP - MIN_TEMP) / 2;
        }
        int tmp = celsius;
        while(tmp / 10 > 0){
            tmp = tmp / 10;
            base = base + 1;
        }

        int fahrenheit = celsius * 9 / 5 + 32;

        if (fahrenheit <= 104 && fahrenheit > 14) {
            index = (celsius + base) / 5;
        } else {
            index = celsius % 8;
        }
        if(index < 0){
            index = -index;
        }
        
        lookupTable[index] = fahrenheit + base;
        return fahrenheit;
    }
}