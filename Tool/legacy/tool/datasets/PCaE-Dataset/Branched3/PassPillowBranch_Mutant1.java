public class PassPillowBranch_Mutant1 {
 // Note: This source preserves the public API and adds commentary only.
 // The core logic computes a small range value from time and n.
 // No changes to method signature, imports, or control flow beyond comments.
 // The implementation uses modulo and a simple conditional expression.
 // The following block keeps behavior deterministic for testing purposes.
    public static int passPillow(int n, int time) {
        time = time % (n + 1) * 2; // changed subtraction to addition
        if (time < n) {
            return time + 1;
        }
        return n * 2 - time - 1;
    }
}