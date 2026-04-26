package kalah;

/**
 * Hauptprogramm für KalahMuster.
 *
 * @since 29.3.2021
 * @author oliverbittel
 */
public class Kalah {

    private static final String ANSI_BLUE = "\u001B[34m";

    public static void main(String[] args) {
        testExample();
        //testHHGame();
        testMiniMaxAndAlphaBetaWithGivenBoard();
        //testHumanMiniMax();
        //testHumanMiniMaxAndAlphaBeta();
        //testHumanAlphaBetaOrdered();
        //testNodeCountComparison();
    }

    /**
     * Beispiel von https://de.wikipedia.org/wiki/Kalaha
     */
    public static void testExample() {
        KalahBoard kalahBd = new KalahBoard(new int[]{5, 3, 2, 1, 2, 0, 0, 4, 3, 0, 1, 2, 2, 0}, 'B');
        kalahBd.print();

        System.out.println("B spielt Mulde 11");
        kalahBd.move(11);
        kalahBd.print();

        System.out.println("B darf nochmals ziehen und spielt Mulde 7");
        kalahBd.move(7);
        kalahBd.print();
    }

    /**
     * Mensch gegen Mensch
     */
    public static void testHHGame() {
        KalahBoard kalahBd = new KalahBoard();
        kalahBd.print();

        while (!kalahBd.isFinished()) {
            int action = kalahBd.readAction();
            kalahBd.move(action);
            kalahBd.print();
        }

        System.out.println("\n" + ANSI_BLUE + "GAME OVER");
    }

    /**
     * Aufgabe b): KI (Minimax) spielt A, Mensch spielt B.
     */
    public static void testMiniMaxAndAlphaBetaWithGivenBoard() {
        KalahBoard kalahBd = new KalahBoard(new int[]{2, 0, 4, 3, 2, 0, 0, 1, 0, 1, 3, 2, 1, 0}, 'A');
        // A ist am Zug und kann aufgrund von Bonuszügen 8-mal hintereinander ziehen!
        // A muss deutlich gewinnen!
        kalahBd.print();

        KalahAI ai = new KalahAI();

        while (!kalahBd.isFinished()) {
            int action;
            if (kalahBd.getCurPlayer() == 'A') {
                action = ai.getBestActionMinimax(kalahBd);
                System.out.println("KI-Minimax (A) spielt Mulde: " + action
                        + "  [Knoten: " + ai.getMinimaxNodeCount() + "]");
            } else {
                action = kalahBd.readAction();
            }
            kalahBd.move(action);
            kalahBd.print();
        }

        printResult(kalahBd);
    }

    /**
     * Aufgabe c): KI (Alpha-Beta) spielt A, Mensch spielt B.
     */
    public static void testHumanMiniMax() {
        KalahBoard kalahBd = new KalahBoard();
        kalahBd.print();

        KalahAI ai = new KalahAI();

        while (!kalahBd.isFinished()) {
            int action;
            if (kalahBd.getCurPlayer() == 'A') {
                action = ai.getBestActionAlphaBeta(kalahBd);
                System.out.println("KI-AlphaBeta (A) spielt Mulde: " + action
                        + "  [Knoten: " + ai.getAlphaBetaNodeCount() + "]");
            } else {
                action = kalahBd.readAction();
            }
            kalahBd.move(action);
            kalahBd.print();
        }

        printResult(kalahBd);
    }

    /**
     * Aufgabe d+e): Mensch gegen KI mit Alpha-Beta + Zugreihenfolge.
     * Wer gewinnt meistens?
     */
    public static void testHumanMiniMaxAndAlphaBeta() {
        KalahBoard kalahBd = new KalahBoard();
        kalahBd.print();

        KalahAI ai = new KalahAI();

        while (!kalahBd.isFinished()) {
            int action;
            if (kalahBd.getCurPlayer() == 'A') {
                action = ai.getBestActionAlphaBetaOrdered(kalahBd);
                System.out.println("KI-AlphaBeta+Order (A) spielt Mulde: " + action
                        + "  [Knoten: " + ai.getAlphaBetaOrderedNodeCount() + "]");
            } else {
                action = kalahBd.readAction();
            }
            kalahBd.move(action);
            kalahBd.print();
        }

        printResult(kalahBd);
    }

    /**
     * Aufgabe e): Mensch (A) gegen stärkste KI (B) mit Alpha-Beta + Zugreihenfolge.
     */
    public static void testHumanAlphaBetaOrdered() {
        KalahBoard kalahBd = new KalahBoard();
        kalahBd.print();

        KalahAI ai = new KalahAI();

        while (!kalahBd.isFinished()) {
            int action;
            if (kalahBd.getCurPlayer() == 'B') {
                action = ai.getBestActionAlphaBetaOrdered(kalahBd);
                System.out.println("KI-AlphaBeta+Order (B) spielt Mulde: " + action
                        + "  [Knoten: " + ai.getAlphaBetaOrderedNodeCount() + "]");
            } else {
                action = kalahBd.readAction();
            }
            kalahBd.move(action);
            kalahBd.print();
        }

        printResult(kalahBd);
    }

    /**
     * Aufgabe f): Vergleicht Knotenanzahl von Minimax, Alpha-Beta und Alpha-Beta+Order
     * auf demselben Startbrett ohne Benutzereingabe (KI vs KI).
     */
    public static void testNodeCountComparison() {
        System.out.println("\n=== Aufgabe f): Knotenvergleich (KI vs KI, 10 Züge) ===");

        KalahAI ai = new KalahAI();

        // Minimax
        KalahBoard bd1 = new KalahBoard(new int[]{2, 0, 4, 3, 2, 0, 0, 1, 0, 1, 3, 2, 1, 0}, 'A');
        long totalMinimax = 0;
        int movesMinimax = 0;
        while (!bd1.isFinished()) {
            char cur = bd1.getCurPlayer();
            int action = ai.getBestActionMinimax(bd1);
            totalMinimax += ai.getMinimaxNodeCount();
            movesMinimax++;
            bd1.move(action);
            // Gegner (B) spielt auch per Minimax
            if (!bd1.isFinished() && bd1.getCurPlayer() != cur) {
                action = ai.getBestActionMinimax(bd1);
                totalMinimax += ai.getMinimaxNodeCount();
                movesMinimax++;
                bd1.move(action);
            }
        }

        // Alpha-Beta
        KalahBoard bd2 = new KalahBoard(new int[]{2, 0, 4, 3, 2, 0, 0, 1, 0, 1, 3, 2, 1, 0}, 'A');
        long totalAlphaBeta = 0;
        int movesAlphaBeta = 0;
        while (!bd2.isFinished()) {
            int action = ai.getBestActionAlphaBeta(bd2);
            totalAlphaBeta += ai.getAlphaBetaNodeCount();
            movesAlphaBeta++;
            bd2.move(action);
        }

        // Alpha-Beta + Order
        KalahBoard bd3 = new KalahBoard(new int[]{2, 0, 4, 3, 2, 0, 0, 1, 0, 1, 3, 2, 1, 0}, 'A');
        long totalOrdered = 0;
        int movesOrdered = 0;
        while (!bd3.isFinished()) {
            int action = ai.getBestActionAlphaBetaOrdered(bd3);
            totalOrdered += ai.getAlphaBetaOrderedNodeCount();
            movesOrdered++;
            bd3.move(action);
        }

        System.out.printf("Minimax          : %d Züge, %d Knoten gesamt, %.1f Knoten/Zug%n",
                movesMinimax, totalMinimax, (double) totalMinimax / movesMinimax);
        System.out.printf("Alpha-Beta       : %d Züge, %d Knoten gesamt, %.1f Knoten/Zug%n",
                movesAlphaBeta, totalAlphaBeta, (double) totalAlphaBeta / movesAlphaBeta);
        System.out.printf("Alpha-Beta+Order : %d Züge, %d Knoten gesamt, %.1f Knoten/Zug%n",
                movesOrdered, totalOrdered, (double) totalOrdered / movesOrdered);
    }

    private static void printResult(KalahBoard board) {
        System.out.println("\n" + ANSI_BLUE + "GAME OVER");
        System.out.println("Kalah A: " + board.getAKalah() + "  |  Kalah B: " + board.getBKalah());
        if (board.getAKalah() > board.getBKalah()) {
            System.out.println("Gewinner: Spieler A");
        } else if (board.getBKalah() > board.getAKalah()) {
            System.out.println("Gewinner: Spieler B");
        } else {
            System.out.println("Unentschieden!");
        }
    }
}
