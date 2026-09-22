public class StudentGrader {
    public static String calculateGrade(int score) {
        String gradeStr = null;
        int MAX_SCORE = 90;
        int MIN_SCORE = 40;
        int curve = 0;
        if (score < MIN_SCORE) {
            curve = curve - (MIN_SCORE - score);
            score = MIN_SCORE;
            char l = 'G';
            gradeStr = String.valueOf(l);
        } else {
            curve = curve + 2;
        }

        if (score > MAX_SCORE) {
            score = MAX_SCORE;
            gradeStr = new String("A - " + score);
            return gradeStr;
        }

        if(score < MAX_SCORE) {
            curve = curve + 8;
            char level = 'F';
            while(score > MIN_SCORE) {
                score = score - 10;
                level--;
            }
            gradeStr = new String(String.valueOf(level));
            if(curve % 2 == 0) {
                score = score + 1;
            }
        }
        gradeStr = gradeStr.toLowerCase();
        gradeStr = gradeStr + ": " + score;
        return gradeStr;
    }
}