
import tkinter as tk
import numpy as np
import random


# =====================================================
#                  SUDOKU GENERATOR
# =====================================================

def generate_solution():

    base = np.array([
        [(r * 3 + r // 3 + c) % 9 + 1 for c in range(9)]
        for r in range(9)
    ])

    bands = list(range(3))
    stacks = list(range(3))

    random.shuffle(bands)
    random.shuffle(stacks)

    rows = []
    cols = []

    for band in bands:
        group = list(range(band * 3, band * 3 + 3))
        random.shuffle(group)
        rows.extend(group)

    for stack in stacks:
        group = list(range(stack * 3, stack * 3 + 3))
        random.shuffle(group)
        cols.extend(group)

    rows = [
        rows[b * 3 + i]
        for b in range(3)
        for i in range(3)
    ]

    cols = [
        cols[s * 3 + i]
        for s in range(3)
        for i in range(3)
    ]

    board = base[np.ix_(rows, cols)]

    digits = random.sample(range(1, 10), 9)
    mapping = {i + 1: digits[i] for i in range(9)}

    return np.vectorize(mapping.get)(board)


def count_solutions(board, limit=2):

    empty = np.argwhere(board == 0)

    if len(empty) == 0:
        return 1

    best_cell = None
    best_candidates = None

    for r, c in empty:

        used = set(board[r, :]) | set(board[:, c])

        br = (r // 3) * 3
        bc = (c // 3) * 3

        used |= set(
            board[br:br + 3, bc:bc + 3].flatten()
        )

        candidates = [
            n for n in range(1, 10)
            if n not in used
        ]

        if not candidates:
            return 0

        if (
            best_candidates is None
            or len(candidates) < len(best_candidates)
        ):
            best_cell = (r, c)
            best_candidates = candidates

    r, c = best_cell
    total = 0

    for num in best_candidates:

        board[r, c] = num

        total += count_solutions(
            board,
            limit - total
        )

        board[r, c] = 0

        if total >= limit:
            return total

    return total


def generate_puzzle(difficulty):

    solution = generate_solution()
    puzzle = solution.copy()

    blanks = {
        "Easy": 35,
        "Medium": 45,
        "Hard": 52
    }

    target = blanks[difficulty]

    cells = [
        (r, c)
        for r in range(9)
        for c in range(9)
    ]

    random.shuffle(cells)

    removed = 0

    for r, c in cells:

        if removed >= target:
            break

        old_value = puzzle[r, c]

        puzzle[r, c] = 0

        if count_solutions(puzzle.copy()) == 1:
            removed += 1
        else:
            puzzle[r, c] = old_value

    return puzzle, solution


# =====================================================
#                    SUDOKU GAME
# =====================================================

class SudokuGame:

    def __init__(self, root):

        self.root = root

        self.root.title("Sudoku")
        self.root.geometry("480x660")
        self.root.resizable(False, False)
        self.root.configure(bg="white")

        self.solution = None
        self.puzzle = None

        self.entries = []

        self.mistakes = 0
        self.max_mistakes = 3

        self.elapsed_time = 0
        self.timer_running = False
        self.timer_job = None

        self.last_checked = {}

        self.create_widgets()
        self.new_game()

    # =================================================
    #                     GUI
    # =================================================

    def create_widgets(self):

        # ---------------- TOP BAR ----------------

        top = tk.Frame(
            self.root,
            bg="white"
        )

        top.pack(
            fill="x",
            padx=30,
            pady=(20, 12)
        )

        tk.Label(
            top,
            text="Difficulty:",
            font=("Arial", 10),
            bg="white",
            fg="#40536B"
        ).pack(side="left")

        self.difficulty = tk.StringVar(value="Easy")

        difficulty_menu = tk.OptionMenu(
            top,
            self.difficulty,
            "Easy",
            "Medium",
            "Hard"
        )

        difficulty_menu.config(
            font=("Arial", 10),
            bg="white",
            fg="#40536B",
            activebackground="white",
            activeforeground="#40536B",
            relief="flat",
            highlightthickness=0,
            bd=0
        )

        difficulty_menu["menu"].config(
            font=("Arial", 10),
            bg="white",
            fg="#40536B"
        )

        difficulty_menu.pack(side="left")

        # Check for mistakes toggle

        self.auto_check = tk.BooleanVar(value=True)

        tk.Checkbutton(
            top,
            text="Check for Mistakes",
            variable=self.auto_check,
            font=("Arial", 9),
            bg="white",
            fg="#718096",
            activebackground="white",
            selectcolor="white",
            relief="flat",
            bd=0,
            highlightthickness=0
        ).pack(side="right")

        # ---------------- SUDOKU GRID ----------------

        self.grid_frame = tk.Canvas(
            self.root,
            width=420,
            height=420,
            bg="white",
            highlightthickness=0
        )

        self.grid_frame.pack(pady=5)

        self.entries = []

        vcmd = (
            self.root.register(self.validate_input),
            "%P"
        )

        cell_size = 420 / 9

        for r in range(9):

            row = []

            for c in range(9):

                cell = tk.Entry(
                    self.grid_frame,
                    width=2,
                    font=("Arial", 20),
                    justify="center",
                    relief="flat",
                    bd=0,
                    bg="white",
                    fg="#60758D",
                    insertbackground="#40536B",
                    validate="key",
                    validatecommand=vcmd
                )

                x = c * cell_size + cell_size / 2
                y = r * cell_size + cell_size / 2

                self.grid_frame.create_window(
                    x,
                    y,
                    window=cell,
                    width=cell_size - 3,
                    height=cell_size - 3
                )

                cell.bind(
                    "<KeyRelease>",
                    lambda event, row=r, col=c:
                    self.check_mistake(row, col)
                )

                row.append(cell)

            self.entries.append(row)

        # Draw grid lines

        for i in range(10):

            position = i * cell_size

            line_width = 2 if i % 3 == 0 else 1

            color = (
                "#52677F"
                if i % 3 == 0
                else "#D6DDE5"
            )

            self.grid_frame.create_line(
                position, 0,
                position, 420,
                fill=color,
                width=line_width
            )

            self.grid_frame.create_line(
                0, position,
                420, position,
                fill=color,
                width=line_width
            )

        # ---------------- TIMER AND MISTAKES ----------------

        info = tk.Frame(
            self.root,
            bg="white"
        )

        info.pack(
            fill="x",
            padx=35,
            pady=10
        )

        self.timer_label = tk.Label(
            info,
            text="Time: 00:00",
            font=("Arial", 11),
            bg="white",
            fg="#60758D"
        )

        self.timer_label.pack(side="left")

        self.mistake_label = tk.Label(
            info,
            text="Mistakes: 0/3",
            font=("Arial", 11),
            bg="white",
            fg="#60758D"
        )

        self.mistake_label.pack(side="right")

        # ---------------- BUTTONS ----------------

        buttons = tk.Frame(
            self.root,
            bg="white"
        )

        buttons.pack(pady=10)

        button_data = [
            ("Check", self.check_board),
            ("Reset", self.reset_board),
            ("Solve", self.solve_board),
            ("New Game", self.new_game)
        ]

        for name, command in button_data:

            tk.Button(
                buttons,
                text=name,
                command=command,
                font=("Arial", 9),
                bg="#F1F4F8",
                fg="#40536B",
                activebackground="#E1E7EF",
                activeforeground="#263A59",
                relief="flat",
                bd=0,
                cursor="hand2",
                padx=10,
                pady=7
            ).pack(
                side="left",
                padx=3
            )

        # ---------------- STATUS MESSAGE ----------------

        self.status = tk.Label(
            self.root,
            text="Good luck! Enjoy your game.",
            font=("Arial", 11, "bold"),
            bg="#EAF0F7",
            fg="#405875",
            width=48,
            height=2,
            relief="flat",
            anchor="center"
        )

        self.status.pack(
            pady=12,
            padx=25,
            fill="x"
        )

    # =================================================
    #                STATUS MESSAGE SYSTEM
    # =================================================

    def show_status(self, message, status_type="info"):

        colors = {

            "success": {
                "bg": "#E1F2E5",
                "fg": "#24613B"
            },

            "warning": {
                "bg": "#FFF2D6",
                "fg": "#91651D"
            },

            "error": {
                "bg": "#FCE5E5",
                "fg": "#A43D3D"
            },

            "info": {
                "bg": "#EAF0F7",
                "fg": "#405875"
            }
        }

        selected = colors[status_type]

        self.status.config(
            text=message,
            bg=selected["bg"],
            fg=selected["fg"]
        )

    # =================================================
    #                 INPUT VALIDATION
    # =================================================

    def validate_input(self, value):

        if value == "":
            return True

        return (
            value.isdigit()
            and len(value) == 1
            and value in "123456789"
        )

    # =================================================
    #                       TIMER
    # =================================================

    def update_timer(self):

        if not self.timer_running:
            return

        minutes = self.elapsed_time // 60
        seconds = self.elapsed_time % 60

        self.timer_label.config(
            text=f"Time: {minutes:02d}:{seconds:02d}"
        )

        self.elapsed_time += 1

        self.timer_job = self.root.after(
            1000,
            self.update_timer
        )

    def start_timer(self):

        self.stop_timer()

        self.elapsed_time = 0
        self.timer_running = True

        self.timer_label.config(text="Time: 00:00")

        self.update_timer()

    def stop_timer(self):

        self.timer_running = False

        if self.timer_job is not None:

            self.root.after_cancel(
                self.timer_job
            )

            self.timer_job = None

    # =================================================
    #                     NEW GAME
    # =================================================

    def new_game(self):

        self.stop_timer()

        selected = self.difficulty.get()

        self.puzzle, self.solution = generate_puzzle(
            selected
        )

        self.mistakes = 0
        self.last_checked = {}

        self.mistake_label.config(
            text="Mistakes: 0/3"
        )

        for r in range(9):

            for c in range(9):

                cell = self.entries[r][c]

                cell.config(state="normal")
                cell.delete(0, tk.END)

                value = self.puzzle[r, c]

                if value != 0:

                    cell.insert(0, str(value))

                    cell.config(
                        state="disabled",
                        disabledbackground="#F1F4F8",
                        disabledforeground="#52677F"
                    )

                else:

                    cell.config(
                        state="normal",
                        bg="white",
                        fg="#60758D"
                    )

        self.show_status(
            f"{selected} puzzle started! Good luck.",
            "info"
        )

        self.start_timer()

    # =================================================
    #                 MISTAKE COUNTER
    # =================================================

    def check_mistake(self, r, c):

        if self.puzzle[r, c] != 0:
            return

        if not self.timer_running:
            return

        if not self.auto_check.get():
            return

        value = self.entries[r][c].get()

        # Empty cell

        if not value:

            self.last_checked.pop((r, c), None)

            self.entries[r][c].config(
                bg="white"
            )

            return

        # Avoid counting the same incorrect value twice

        previous = self.last_checked.get((r, c))

        if previous == value:
            return

        self.last_checked[(r, c)] = value

        # Incorrect entry

        if int(value) != self.solution[r, c]:

            self.mistakes += 1

            self.mistake_label.config(
                text=f"Mistakes: {self.mistakes}/3"
            )

            self.entries[r][c].config(
                bg="#F8CACA"
            )

            if self.mistakes >= self.max_mistakes:

                self.game_over()

            else:

                self.show_status(
                    f"Incorrect entry! Mistakes: {self.mistakes}/3",
                    "error"
                )

        # Correct entry

        else:

            self.entries[r][c].config(
                bg="#D5F0DD"
            )

            self.show_status(
                "Correct entry! Keep going.",
                "success"
            )

    # =================================================
    #                     GAME OVER
    # =================================================

    def game_over(self):

        self.stop_timer()

        for row in self.entries:

            for cell in row:

                cell.config(
                    state="disabled"
                )

        self.show_status(
            "GAME OVER! Start a new game to play again.",
            "error"
        )

    # =================================================
    #                    GET BOARD
    # =================================================

    def get_board(self):

        board = np.zeros(
            (9, 9),
            dtype=int
        )

        for r in range(9):

            for c in range(9):

                value = self.entries[r][c].get()

                if value:
                    board[r, c] = int(value)

        return board

    # =================================================
    #                    CHECK BOARD
    # =================================================

    def check_board(self):

        if not self.timer_running:
            return

        board = self.get_board()

        incorrect = 0
        empty = 0

        for r in range(9):

            for c in range(9):

                cell = self.entries[r][c]

                if self.puzzle[r, c] != 0:
                    continue

                value = board[r, c]

                if value == 0:

                    cell.config(bg="white")
                    empty += 1

                elif value != self.solution[r, c]:

                    cell.config(bg="#F8CACA")
                    incorrect += 1

                else:

                    cell.config(bg="#D5F0DD")

        if incorrect == 0 and empty == 0:

            self.stop_timer()

            self.show_status(
                "Congratulations! Puzzle solved!",
                "success"
            )

        elif incorrect > 0:

            self.show_status(
                f"{incorrect} incorrect entries found!",
                "error"
            )

        else:

            self.show_status(
                f"Keep going! {empty} cells remaining.",
                "warning"
            )

    # =================================================
    #                    RESET BOARD
    # =================================================

    def reset_board(self):

        if not self.timer_running:
            return

        self.last_checked = {}

        for r in range(9):

            for c in range(9):

                if self.puzzle[r, c] == 0:

                    cell = self.entries[r][c]

                    cell.delete(0, tk.END)

                    cell.config(
                        bg="white"
                    )

        self.show_status(
            "Board reset successfully!",
            "info"
        )

    # =================================================
    #                    SOLVE BOARD
    # =================================================

    def solve_board(self):

        if self.solution is None:
            return

        self.stop_timer()

        for r in range(9):

            for c in range(9):

                cell = self.entries[r][c]

                cell.config(state="normal")

                cell.delete(0, tk.END)

                cell.insert(
                    0,
                    str(self.solution[r, c])
                )

                cell.config(
                    state="disabled",
                    disabledbackground="#E1F2E5",
                    disabledforeground="#24613B"
                )

        self.show_status(
            "Solution revealed!",
            "success"
        )


# =====================================================
#                       RUN GAME
# =====================================================

if __name__ == "__main__":

    root = tk.Tk()

    game = SudokuGame(root)

    root.mainloop()
