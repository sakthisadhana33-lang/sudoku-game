# Sudoku Game

A desktop Sudoku game built with Python, Tkinter, and NumPy.

## Overview

This project provides an interactive Sudoku experience through a graphical user interface. It generates Sudoku puzzles at different difficulty levels and lets the player enter answers, track time, and check their progress.

## Features

- 9 × 9 interactive Sudoku board
- Easy, Medium, and Hard difficulty levels
- Puzzle generation from a completed valid Sudoku solution
- Solution-count checking to help ensure generated puzzles have a unique solution
- Input validation and mistake tracking
- Timer
- Check, Reset, Solve, and New Game controls
- In-window status messages

## Technologies Used

- Python – application logic
- Tkinter – desktop graphical user interface
- NumPy – representation and manipulation of the Sudoku board using a 2D array

## Concepts Demonstrated

- Event-driven programming with GUI callbacks and keyboard events
- Two-dimensional arrays
- Recursion and backtracking
- Sudoku constraint checking
- Basic GUI design and state management

## Requirements

- Python 3
- NumPy

Tkinter is included with many standard Python installations. On some Linux systems, it may need to be installed separately through the operating system's package manager.

Install NumPy:

```bash
python -m pip install numpy
```

## Run the Project

1. Clone or download this repository.
2. Open the project folder in VS Code.
3. Install the required dependency.
4. Run the Python file containing the application entry point.

For example, if your main file is named `sudoku.py`:

```bash
python sudoku.py
```

If your main Python file has a different name, use that filename instead.

## How to Play

1. Launch the application.
2. Choose a difficulty level and start a new game.
3. Enter numbers into the empty cells.
4. Use the available controls to check your board, reset your entries, or view the solution.
5. Complete the puzzle while following standard Sudoku rules: each row, column, and 3 × 3 box must contain the digits 1–9 without repetition.

## Future Improvements
- Add a puzzle library with more difficulty variations.
- Improve difficulty assessment based on the solving techniques required.
- Add keyboard navigation between cells.
- Add persistent game statistics.

## Author
KN Sakthi Sadhana

