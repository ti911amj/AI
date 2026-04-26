package kalah;

import java.util.Comparator;
import java.util.List;

public class KalahAI {

    private static final int DEPTH = 5;

    private int minimaxNodeCount;
    private int alphaBetaNodeCount;
    private int alphaBetaOrderedNodeCount;

    public int getMinimaxNodeCount()      { return minimaxNodeCount; }
    public int getAlphaBetaNodeCount()    { return alphaBetaNodeCount; }
    public int getAlphaBetaOrderedNodeCount() { return alphaBetaOrderedNodeCount; }

    // -------------------------------------------------------------------------
    // Aufgabe b): Minimax
    // -------------------------------------------------------------------------

    public int getBestActionMinimax(KalahBoard board) {
        minimaxNodeCount = 0;
        char maxPlayer = board.getCurPlayer();

        List<KalahBoard> actions = board.possibleActions();
        int bestValue = Integer.MIN_VALUE;
        int bestAction = -1;

        for (KalahBoard next : actions) {
            int value = minimax(next, DEPTH - 1, maxPlayer);
            if (value > bestValue) {
                bestValue = value;
                bestAction = next.getLastPlay();
            }
        }
        return bestAction;
    }

    private int minimax(KalahBoard board, int depth, char maxPlayer) {
        minimaxNodeCount++;

        if (depth == 0 || board.isFinished()) {
            return evaluate(board, maxPlayer);
        }

        List<KalahBoard> actions = board.possibleActions();
        if (actions.isEmpty()) {
            return evaluate(board, maxPlayer);
        }

        if (board.getCurPlayer() == maxPlayer) {
            int best = Integer.MIN_VALUE;
            for (KalahBoard next : actions) {
                int val = minimax(next, depth - 1, maxPlayer);
                if (val > best) best = val;
            }
            return best;
        } else {
            int best = Integer.MAX_VALUE;
            for (KalahBoard next : actions) {
                int val = minimax(next, depth - 1, maxPlayer);
                if (val < best) best = val;
            }
            return best;
        }
    }

    // -------------------------------------------------------------------------
    // Aufgabe c): Alpha-Beta-Pruning
    // -------------------------------------------------------------------------

    public int getBestActionAlphaBeta(KalahBoard board) {
        alphaBetaNodeCount = 0;
        char maxPlayer = board.getCurPlayer();

        List<KalahBoard> actions = board.possibleActions();
        int bestValue = Integer.MIN_VALUE;
        int bestAction = -1;

        for (KalahBoard next : actions) {
            int value = alphaBeta(next, DEPTH - 1, Integer.MIN_VALUE, Integer.MAX_VALUE, maxPlayer);
            if (value > bestValue) {
                bestValue = value;
                bestAction = next.getLastPlay();
            }
        }
        return bestAction;
    }

    private int alphaBeta(KalahBoard board, int depth, int alpha, int beta, char maxPlayer) {
        alphaBetaNodeCount++;

        if (depth == 0 || board.isFinished()) {
            return evaluate(board, maxPlayer);
        }

        List<KalahBoard> actions = board.possibleActions();
        if (actions.isEmpty()) {
            return evaluate(board, maxPlayer);
        }

        if (board.getCurPlayer() == maxPlayer) {
            int best = Integer.MIN_VALUE;
            for (KalahBoard next : actions) {
                int val = alphaBeta(next, depth - 1, alpha, beta, maxPlayer);
                if (val > best) best = val;
                if (best > alpha) alpha = best;
                if (alpha >= beta) break; // Beta-Schnitt
            }
            return best;
        } else {
            int best = Integer.MAX_VALUE;
            for (KalahBoard next : actions) {
                int val = alphaBeta(next, depth - 1, alpha, beta, maxPlayer);
                if (val < best) best = val;
                if (best < beta) beta = best;
                if (alpha >= beta) break; // Alpha-Schnitt
            }
            return best;
        }
    }

    // -------------------------------------------------------------------------
    // Aufgabe d): Alpha-Beta + Zugreihenfolge-Heuristik
    // Züge werden vor der Rekursion nach evaluate() vorsortiert:
    // Max-Knoten: beste Züge zuerst → mehr Beta-Schnitte
    // Min-Knoten: schlechteste Züge zuerst → mehr Alpha-Schnitte
    // -------------------------------------------------------------------------

    public int getBestActionAlphaBetaOrdered(KalahBoard board) {
        alphaBetaOrderedNodeCount = 0;
        char maxPlayer = board.getCurPlayer();

        List<KalahBoard> actions = board.possibleActions();
        actions.sort(Comparator.comparingInt(b -> -evaluate(b, maxPlayer))); // beste zuerst

        int bestValue = Integer.MIN_VALUE;
        int bestAction = -1;

        for (KalahBoard next : actions) {
            int value = alphaBetaOrdered(next, DEPTH - 1, Integer.MIN_VALUE, Integer.MAX_VALUE, maxPlayer);
            if (value > bestValue) {
                bestValue = value;
                bestAction = next.getLastPlay();
            }
        }
        return bestAction;
    }

    private int alphaBetaOrdered(KalahBoard board, int depth, int alpha, int beta, char maxPlayer) {
        alphaBetaOrderedNodeCount++;

        if (depth == 0 || board.isFinished()) {
            return evaluate(board, maxPlayer);
        }

        List<KalahBoard> actions = board.possibleActions();
        if (actions.isEmpty()) {
            return evaluate(board, maxPlayer);
        }

        if (board.getCurPlayer() == maxPlayer) {
            // Beste Züge zuerst → mehr Beta-Schnitte
            actions.sort(Comparator.comparingInt(b -> -evaluate(b, maxPlayer)));
            int best = Integer.MIN_VALUE;
            for (KalahBoard next : actions) {
                int val = alphaBetaOrdered(next, depth - 1, alpha, beta, maxPlayer);
                if (val > best) best = val;
                if (best > alpha) alpha = best;
                if (alpha >= beta) break;
            }
            return best;
        } else {
            // Schlechteste Züge (für maxPlayer) zuerst → mehr Alpha-Schnitte
            actions.sort(Comparator.comparingInt(b -> evaluate(b, maxPlayer)));
            int best = Integer.MAX_VALUE;
            for (KalahBoard next : actions) {
                int val = alphaBetaOrdered(next, depth - 1, alpha, beta, maxPlayer);
                if (val < best) best = val;
                if (best < beta) beta = best;
                if (alpha >= beta) break;
            }
            return best;
        }
    }

    // -------------------------------------------------------------------------
    // Heuristik: Kalah-Differenz aus Sicht von 'player'
    // -------------------------------------------------------------------------

    public int evaluate(KalahBoard board, char player) {
        if (player == KalahBoard.APlayer) {
            return board.getAKalah() - board.getBKalah();
        } else {
            return board.getBKalah() - board.getAKalah();
        }
    }
}
