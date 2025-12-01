# 15-puzzle greedy solver

GOAL_BOARD = [1, 2, 3, 4,
              5, 6, 7, 8,
              9, 10, 11, 12,
              13, 14, 15, 0]


def compute_manhattan_total(board):
    """
    This computes the total "Manhattan distance" of the board.
    For each tile, it measures how far the tile is from where it should be
    in the goal board, using only up/down/left/right movement.
    The empty tile (0) is ignored.
    """
    total_distance = 0
    for position in range(16):
        tile_value = board[position]
        if tile_value == 0:
            continue  # The empty tile does not contribute to the distance.

        current_row = position // 4
        current_column = position % 4

        goal_position = tile_value - 1
        goal_row = goal_position // 4
        goal_column = goal_position % 4

        distance = abs(current_row - goal_row) + abs(current_column - goal_column)
        total_distance += distance

    return total_distance


def generate_all_neighbor_boards(board):
    """
    This produces all boards that can be reached from the current board
    by sliding a single tile into the empty position.
    """
    list_of_neighbors = []

    index_of_empty = board.index(0)
    empty_row = index_of_empty // 4
    empty_column = index_of_empty % 4

    possible_shifts = []

    # If the empty space is not on the top row, a tile may slide down into it.
    if empty_row > 0:
        possible_shifts.append(-4)

    # If the empty space is not on the bottom row, a tile may slide up into it.
    if empty_row < 3:
        possible_shifts.append(4)

    # If the empty space is not in the leftmost column, a tile may slide right into it.
    if empty_column > 0:
        possible_shifts.append(-1)

    # If the empty space is not in the rightmost column, a tile may slide left into it.
    if empty_column < 3:
        possible_shifts.append(1)

    # For each allowed shift, create a new board with the empty tile swapped.
    for shift in possible_shifts:
        new_empty_position = index_of_empty + shift

        new_board = board[:]  # Make a copy of the board.
        temporary = new_board[index_of_empty]
        new_board[index_of_empty] = new_board[new_empty_position]
        new_board[new_empty_position] = temporary

        list_of_neighbors.append(new_board)

    return list_of_neighbors


def print_board_in_grid(board):
    """Print the 4×4 board in a clear rectangular form."""
    for row in range(4):
        row_values = board[4 * row : 4 * row + 4]
        line = ""
        for tile_value in row_values:
            if tile_value == 0:
                line += "  ."
            else:
                line += f"{tile_value:3}"
        print(line)
    print()


def boards_are_equal(board_a, board_b):
    """Return True if both boards contain exactly the same numbers in order."""
    for position in range(16):
        if board_a[position] != board_b[position]:
            return False
    return True


def find_board_index(list_of_all_boards, board):
    """
    Given a list of boards, return the index of 'board' if it exists.
    Otherwise return -1.
    """
    for index in range(len(list_of_all_boards)):
        if boards_are_equal(list_of_all_boards[index], board):
            return index
    return -1


def greedy_best_first_search(starting_board, maximum_number_of_expansions=100000):
    """
    This performs a very simple greedy search.
    At each step, it chooses the board with the smallest Manhattan distance.
    It does not use any advanced data structures.
    All information is kept in plain lists.

    list_of_all_boards[i] holds a board (a list of 16 integers).
    parent_index[i] holds the index of the board that created board i.
    frontier_indices is a list of indices of boards that have not been expanded yet.
    """
    list_of_all_boards = [starting_board]
    parent_index = [-1]  # The starting board has no parent.
    frontier_indices = [0]  # We begin with only the starting board.

    number_of_expanded_boards = 0

    while len(frontier_indices) > 0 and number_of_expanded_boards < maximum_number_of_expansions:

        
        # Choose board with the smallest Manhattan score.
        
        best_frontier_position = 0
        best_board_index = frontier_indices[0]
        best_board = list_of_all_boards[best_board_index]
        best_score = compute_manhattan_total(best_board)

        for position_in_frontier in range(1, len(frontier_indices)):
            current_index = frontier_indices[position_in_frontier]
            current_board = list_of_all_boards[current_index]
            current_score = compute_manhattan_total(current_board)

            if current_score < best_score:
                best_score = current_score
                best_board_index = current_index
                best_frontier_position = position_in_frontier

        # Remove the chosen board from the frontier.
        frontier_indices.pop(best_frontier_position)
        current_board = list_of_all_boards[best_board_index]

        number_of_expanded_boards += 1

        
        # Check if the current board is the goal.

        if boards_are_equal(current_board, GOAL_BOARD):
            # Reconstruct the path by walking backward through parent links.
            path_indices = []
            index = best_board_index
            while index != -1:
                path_indices.append(index)
                index = parent_index[index]

            path_indices.reverse()  # Now the path goes from start to goal.

            path_of_boards = []
            for index in path_indices:
                path_of_boards.append(list_of_all_boards[index])

            return path_of_boards, number_of_expanded_boards

        
        # The board is not the goal, so expand all neighbors.

        neighbor_boards = generate_all_neighbor_boards(current_board)

        for neighbor in neighbor_boards:
            existing_index = find_board_index(list_of_all_boards, neighbor)
            if existing_index == -1:
                list_of_all_boards.append(neighbor)
                parent_index.append(best_board_index)
                frontier_indices.append(len(list_of_all_boards) - 1)

    return None, number_of_expanded_boards


def read_board_from_user():
    """
    Ask the user to type a 15-puzzle board as 16 integers separated by spaces.
    The empty space is represented by 0.
    """
    print("Enter a 15-puzzle board as 16 integers (0 to 15), separated by spaces.")
    print("Use 0 for the empty square.")
    print("Press Enter with no input to use a prepared example board.")
    user_input = input("Your board: ").strip()

    if user_input == "":
        example_board = [
            5, 1, 2, 3,
            9, 6, 7, 4,
            13, 10, 11, 8,
            0, 14, 15, 12
        ]
        print("\nUsing example board:")
        print_board_in_grid(example_board)
        return example_board

    pieces = user_input.split()
    if len(pieces) != 16:
        raise ValueError("Exactly 16 integers must be given.")

    board = [int(x) for x in pieces]

    sorted_board = board[:]
    sorted_board.sort()
    if sorted_board != list(range(16)):
        raise ValueError("The numbers must be exactly the integers from 0 to 15.")

    return board


def main():
    starting_board = read_board_from_user()
    print("Starting board (score =", compute_manhattan_total(starting_board), "):")
    print_board_in_grid(starting_board)

    print("Goal board:")
    print_board_in_grid(GOAL_BOARD)

    print("Running greedy search (always choosing the smallest Manhattan score)...")
    path, number_expanded = greedy_best_first_search(starting_board)

    print("Number of boards expanded:", number_expanded)

    if path is None:
        print("No solution was found before the limit was reached.")
    else:
        print("Solution found in", len(path) - 1, "moves.")
        print("Showing all boards in the solution path:\n")
        for step_number, board in enumerate(path):
            print("Step", step_number, "(score =", compute_manhattan_total(board), "):")
            print_board_in_grid(board)


if __name__ == "__main__":
    main()
