import random
import copy

N = 9

# Sample incomplete Sudoku puzzle (0 = empty cell)
initial_board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],

    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],

    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# Identify fixed cells (those that cannot be changed)
fixed = [[cell != 0 for cell in row] for row in initial_board]

# Fill board randomly within each 3x3 block
def fill_board_randomly(board):
    board = copy.deepcopy(board)
    for block_row in range(3):
        for block_col in range(3):
            nums = list(range(1, 10))
            # Remove already present numbers in block
            for i in range(3):
                for j in range(3):
                    r = block_row * 3 + i
                    c = block_col * 3 + j
                    if board[r][c] != 0:
                        nums.remove(board[r][c])
            random.shuffle(nums)
            for i in range(3):
                for j in range(3):
                    r = block_row * 3 + i
                    c = block_col * 3 + j
                    if board[r][c] == 0:
                        board[r][c] = nums.pop()
    return board

# Heuristic: total number of conflicts in rows and columns
def compute_heuristic(board):
    conflicts = 0
    for i in range(9):
        row_vals = [0]*10
        col_vals = [0]*10
        for j in range(9):
            row_vals[board[i][j]] += 1
            col_vals[board[j][i]] += 1
        conflicts += sum([v - 1 for v in row_vals if v > 1])
        conflicts += sum([v - 1 for v in col_vals if v > 1])
    return conflicts

# Get all swappable cell pairs in a 3x3 block
def get_swappable_cells(board, block_row, block_col):
    cells = []
    for i in range(3):
        for j in range(3):
            r = block_row * 3 + i
            c = block_col * 3 + j
            if not fixed[r][c]:
                cells.append((r, c))
    return cells

# Generate a neighbor by swapping two values in a block
def get_best_neighbor(board):
    best_board = copy.deepcopy(board)
    best_h = compute_heuristic(board)

    for block_row in range(3):
        for block_col in range(3):
            cells = get_swappable_cells(board, block_row, block_col)
            for i in range(len(cells)):
                for j in range(i+1, len(cells)):
                    (r1, c1), (r2, c2) = cells[i], cells[j]
                    neighbor = copy.deepcopy(board)
                    neighbor[r1][c1], neighbor[r2][c2] = neighbor[r2][c2], neighbor[r1][c1]
                    h = compute_heuristic(neighbor)
                    if h < best_h:
                        best_board = neighbor
                        best_h = h
    return best_board, best_h

# Hill Climbing main function
def hill_climb(initial_board, max_iterations=10000):
    current = fill_board_randomly(initial_board)
    current_h = compute_heuristic(current)

    for step in range(max_iterations):
        if current_h == 0:
            print(f"Solved in {step} steps!")
            return current
        neighbor, neighbor_h = get_best_neighbor(current)
        if neighbor_h >= current_h:
            print("Stuck at local minimum.")
            break
        current = neighbor
        current_h = neighbor_h
    return current

# Print the board
def print_board(board):
    for i in range(N):
        print(" ".join(str(x) if x != 0 else '.' for x in board[i]))
    print()

# Run the solver
if __name__ == "__main__":
    print("Initial Sudoku Puzzle:")
    print_board(initial_board)

    solved = hill_climb(initial_board)

    print("Final Board:")
    print_board(solved)
