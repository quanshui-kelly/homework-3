############################################################
# CIS 521: Homework 3
############################################################

############################################################
# Imports
############################################################
import random
from queue import PriorityQueue
import math
############################################################

student_name = "Xinyuan Quan"

############################################################
# Section 1: Tile Puzzle
############################################################


def create_tile_puzzle(rows, cols):
    ans = []
    for i in range(rows):
        lst_i = []
        for j in range(cols):
            if i == rows - 1 and j == cols - 1:
                lst_i.append(0)
            else:
                lst_i.append(i * cols + j + 1)
        ans.append(lst_i)
    return ans


class TilePuzzle(object):
    def __init__(self, board):
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0])

        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] == 0:
                    self.empty_row = i
                    self.empty_col = j

    def get_board(self):
        return self.board

    def perform_move(self, direction):
        if direction == 'up':
            new_row = self.empty_row - 1
            if 0 <= new_row < self.rows:
                temp = self.board[new_row][self.empty_col]
                self.board[new_row][self.empty_col] = (
                    self.board[self.empty_row][self.empty_col]
                )
                self.board[self.empty_row][self.empty_col] = temp
                self.empty_row = new_row
                return True

        if direction == 'down':
            new_row = self.empty_row + 1
            if 0 <= new_row < self.rows:
                temp = self.board[new_row][self.empty_col]
                self.board[new_row][self.empty_col] = (
                    self.board[self.empty_row][self.empty_col]
                )
                self.board[self.empty_row][self.empty_col] = temp
                self.empty_row = new_row
                return True

        if direction == 'left':
            new_col = self.empty_col - 1
            if 0 <= new_col < self.cols:
                temp = self.board[self.empty_row][new_col]
                self.board[self.empty_row][new_col] = (
                    self.board[self.empty_row][self.empty_col]
                )
                self.board[self.empty_row][self.empty_col] = temp
                self.empty_col = new_col
                return True

        if direction == 'right':
            new_col = self.empty_col + 1
            if 0 <= new_col < self.cols:
                temp = self.board[self.empty_row][new_col]
                self.board[self.empty_row][new_col] = (
                    self.board[self.empty_row][self.empty_col]
                )
                self.board[self.empty_row][self.empty_col] = temp
                self.empty_col = new_col
                return True
        return False

    def scramble(self, num_moves):
        directions = ["up", "down", "left", "right"]

        for i in range(num_moves):
            direction = random.choice(directions)
            self.perform_move(direction)

    def is_solved(self):
        right_ans = create_tile_puzzle(self.rows, self.cols)
        return self.board == right_ans

    def copy(self):
        new_one = []

        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(self.board[i][j])
            new_one.append(row)

        return TilePuzzle(new_one)

    def successors(self):
        directions = ["up", "down", "left", "right"]

        for direction in directions:
            new_puzzle = self.copy()

            if new_puzzle.perform_move(direction):
                yield direction, new_puzzle

    # Required
    def find_solutions_iddfs(self):
        limit = 0

        while True:
            solutions = []
            for solution in self.iddfs_helper(limit, []):
                solutions.append(solution)  # noqa: PERF402

            if len(solutions) > 0:
                for solution in solutions:
                    yield solution
                return

            limit += 1

    def iddfs_helper(self, limit, moves):
        if self.is_solved():
            yield moves
            return

        if limit == 0:
            return

        for direction, new_puzzle in self.successors():
            new_moves = moves + [direction]
            yield from new_puzzle.iddfs_helper(limit - 1, new_moves)

    # Required
    def find_solution_a_star(self):

        queue = PriorityQueue()
        visited = set()
        order = 0

        distance = self.Manhattan_helper()
        queue.put((distance, order, self, []))

        state = tuple(tuple(row) for row in self.get_board())
        visited.add(state)

        while not queue.empty():
            _priority, _, puzzle, moves = queue.get()

            if puzzle.is_solved():
                return moves

            for direction, new_puzzle in puzzle.successors():
                new_moves = moves + [direction]

                distance = new_puzzle.Manhattan_helper()
                f = len(new_moves) + distance

                state = tuple(
                    tuple(row) for row in new_puzzle.get_board()
                )

                if state not in visited:
                    visited.add(state)

                    order += 1
                    queue.put(
                        (f, order, new_puzzle, new_moves)
                    )

    def Manhattan_helper(self):
        distance = 0

        for row in range(self.rows):
            for col in range(self.cols):
                tile = self.board[row][col]

                if tile != 0:
                    for i in range(self.rows):
                        for j in range(self.cols):
                            if i * self.cols + j + 1 == tile:
                                distance += abs(row - i) + abs(col - j)
                                break
        return distance
############################################################
# Section 2: Grid Navigation
############################################################
def find_path(start, goal, scene):


    if scene[start[0]][start[1]]:
        return None

    if scene[goal[0]][goal[1]]:
        return None

    if start == goal:
        return [start]

    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1),
        (-1, -1),
        (-1, 1),
        (1, -1),
        (1, 1)
    ]

    queue = PriorityQueue()
    best_cost = {}
    order = 0

    best_cost[start] = 0
    queue.put((0, order, 0, start, [start]))

    while not queue.empty():
        _priority, _, g, current, path = queue.get()

        if current == goal:
            return path

        for i, j in directions:
            new_row = current[0] + i
            new_col = current[1] + j

            if new_row < 0 or new_row >= len(scene):
                continue

            if new_col < 0 or new_col >= len(scene[0]):
                continue

            if scene[new_row][new_col]:
                continue

            new_position = (new_row, new_col)

            if i != 0 and j != 0:
                step_cost = math.sqrt(2)
            else:
                step_cost = 1

            new_g = g + step_cost

            if (new_position not in best_cost
                    or new_g < best_cost[new_position]):

                best_cost[new_position] = new_g

                new_path = path + [new_position]

                h = math.sqrt(
                    (new_row - goal[0]) ** 2
                    + (new_col - goal[1]) ** 2
                )

                f = new_g + h

                order += 1
                queue.put(
                    (f, order, new_g,
                     new_position, new_path)
                )

    return None

############################################################
# Section 3: Linear Disk Movement, Revisited
############################################################


def solve_distinct_disks(length, n):


    start = []
    for i in range(length):
        if i < n:
            start.append(i + 1)
        else:
            start.append(0)
    start = tuple(start)

    goal = [0] * length
    for i in range(n):
        goal[length - n + i] = n - i
    goal = tuple(goal)

    if start == goal:
        return []

    queue = PriorityQueue()
    order = 0

    h = 0
    for i in range(length):
        disk = start[i]

        if disk != 0:
            target = length - disk
            h += math.ceil(abs(i - target) / 2)

    queue.put((h, order, 0, start, []))

    best_cost = {}
    best_cost[start] = 0

    while not queue.empty():
        _priority, _, g, state, moves = queue.get()

        if state == goal:
            return moves

        for i in range(length):
            if state[i] == 0:
                continue

            new_positions = []
            if i - 1 >= 0 and state[i - 1] == 0:
                new_positions.append(i - 1)

            if i + 1 < length and state[i + 1] == 0:
                new_positions.append(i + 1)

            if (i - 2 >= 0 and
                    state[i - 2] == 0 and
                    state[i - 1] != 0):
                new_positions.append(i - 2)

            if (i + 2 < length and
                    state[i + 2] == 0 and
                    state[i + 1] != 0):
                new_positions.append(i + 2)

            for new_position in new_positions:
                new_state = list(state)

                new_state[new_position] = new_state[i]
                new_state[i] = 0

                new_state = tuple(new_state)

                new_moves = moves + [
                    (i, new_position)
                ]

                new_g = g + 1

                if (new_state not in best_cost or
                        new_g < best_cost[new_state]):

                    best_cost[new_state] = new_g

                    h = 0

                    for j in range(length):
                        disk = new_state[j]

                        if disk != 0:
                            target = length - disk
                            h += math.ceil(
                                abs(j - target) / 2
                            )

                    f = new_g + h

                    order += 1

                    queue.put(
                        (
                            f,
                            order,
                            new_g,
                            new_state,
                            new_moves
                        )
                    )

    return None

############################################################
# Section 4: Feedback
############################################################


# Just an approximation is fine.
feedback_question_1 = """
12
"""

feedback_question_2 = """
Q2 is hard, it contains all parts in one function.
"""

feedback_question_3 = """
We can have a deep understanding of these algorithms after trying for several
times under different scenes.
"""
