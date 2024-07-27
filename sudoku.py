import subprocess
import time
import copy

def parse_board(output_lines):
    """Parse the Sudoku board from the output lines."""
    board = []
    for line in output_lines:
        if len(line.strip().split()) == 13 and all(char in '123456789.|' for char in line.strip().replace(' ', '')):
            cleaned_line = line.replace('|', '').strip()
            board.append(cleaned_line.strip().split())
    return board

def is_valid(board, row, col, num):
    """Check if 'num' is not in the current row, column, and 3x3 subgrid."""
    for c in range(9):
        if board[row][c] == num:
            return False
    for r in range(9):
        if board[r][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if board[r][c] == num:
                return False
    return True

def solve_sudoku(board):
    """Solve the Sudoku puzzle using backtracking."""
    empty_cell = find_empty(board)
    if not empty_cell:
        return True
    row, col = empty_cell
    for num in '123456789':
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = '.'
    return False

def find_empty(board):
    """Find an empty cell in the board (represented by '.')."""
    for r in range(9):
        for c in range(9):
            if board[r][c] == '.':
                return (r, c)
    return None

def best_move(board, new_board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == '.':
                return (r, c, new_board[r][c])
    return None

def run_game(executable_path):
    process = subprocess.Popen([executable_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output_lines = []
    i=0
    j=1
    print("Playing game:", j)
    while True:
        output = process.stdout.readline().strip()
        output_lines.append(output)
        #print(output.strip())  # Print the output for debugging
        #print(i)
        if i%14==0 and i!=0:
            board = parse_board(output_lines)
            new_board = copy.deepcopy(board)
            if solve_sudoku(new_board):
                move = best_move(board, new_board)
                if move:
                    move_str = f"{move[0]} {move[1]} {move[2]}"
                    #print(f"Bot move: {move_str}")
                    process.stdin.write(move_str + "\n")
                    process.stdin.flush()
                else:
                    print("")
            else:
                print("No solution found.")
                break
            output_lines = []
        if "Congratulations" in output:
            i=-2
            j+=1
            if(j<=420):
                print("Playing game:", j)
        if "flag" in output:
            print(output.strip())
            break
        i+=1
# Run the game
executable_path = "./sudoku"
run_game(executable_path)
