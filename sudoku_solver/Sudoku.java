package sudoku;

public class Sudoku {

    private int[][] board;

    public Sudoku(int[][] board) {
        this.board = board;
    }

    private boolean possible(int y, int x, int num) {
        for (int oY = 0; oY < board.length; oY++) {
            if (board[oY][x] == num) return false;
        }
        for (int oX = 0; oX < board.length; oX++) {
            if (board[y][oX] == num) return false;
        }
        for (int oY = y / 3 * 3; oY < y / 3 * 3 + 3; oY++) {
            for (int oX = x / 3 * 3; oX < x / 3 * 3 + 3; oX++) {
                if (board[oY][oX] == num) return false;
            }
        }
        return true;
    }

    public boolean solve() {
        int min = 1;
        int max = 9;
        for (int y = 0; y < board.length; y++) {
            for (int x = 0; x < board[y].length; x++) {
                if (board[y][x] == 0) {
                    for (int k = min; k <= max; k++) {
                        if (possible(y, x, k)) {
                            board[y][x] = k;
                            if (solve()) return true;
                            else board[y][x] = 0;
                        }
                    }
                    return false;
                }
            }
        }
        return true;
    }

    public void printBoard() {
        for (int i = 0; i < board.length; i++) {
            for (int j = 0; j < board[i].length; j++) {
                System.out.print(board[i][j] + "  ");
            }
            System.out.println();
        }
    }

    public int[][] getBoard() {
        return board;
    }
}