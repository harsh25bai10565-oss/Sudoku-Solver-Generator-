#!/usr/bin/env python3
"""
Sudoku Solver & Generator with AI/ML Concepts
- Backtracking search with MRV heuristic and forward checking (AI)
- Difficulty prediction using ML (scikit-learn)
- Puzzle generation with controlled difficulty
"""

import numpy as np
import random
import copy
from collections import defaultdict
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib  # for saving/loading model

# ======================================================
# Part 1: Sudoku Solver with AI Search Techniques
# ======================================================

class SudokuSolver:
    def __init__(self, puzzle):
        self.puzzle = [row[:] for row in puzzle]  # copy
        self.size = 9
        self.box_size = 3
        self.candidates = None   # will hold possible values for each cell

    def solve(self):
        """Solve using backtracking with MRV heuristic and forward checking."""
        self._init_candidates()
        return self._backtrack()

    def _init_candidates(self):
        """Initialize possible candidates for each empty cell."""
        self.candidates = [[set() for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if self.puzzle[i][j] == 0:
                    self.candidates[i][j] = self._get_candidates(i, j)
                else:
                    self.candidates[i][j] = {self.puzzle[i][j]}

    def _get_candidates(self, row, col):
        """Return set of possible numbers for cell (row, col)."""
        used = set()
        # row
        used.update(self.puzzle[row])
        # column
        used.update(self.puzzle[i][col] for i in range(self.size))
        # box
        box_r = (row // self.box_size) * self.box_size
        box_c = (col // self.box_size) * self.box_size
        for i in range(box_r, box_r + self.box_size):
            used.update(self.puzzle[i][box_c:box_c + self.box_size])
        return {x for x in range(1, 10) if x not in used}

    def _backtrack(self):
        """Recursive backtracking with MRV and forward checking."""
        # Find cell with fewest candidates (MRV heuristic)
        min_cell = None
        min_candidates = float('inf')
        for i in range(self.size):
            for j in range(self.size):
                if self.puzzle[i][j] == 0:
                    cand_count = len(self.candidates[i][j])
                    if cand_count < min_candidates:
                        min_candidates = cand_count
                        min_cell = (i, j)
                        if min_candidates == 1:
                            break
            if min_candidates == 1:
                break

        if min_cell is None:
            return True  # solved

        row, col = min_cell
        # Try each candidate in order (could also use heuristic, e.g., least constraining value)
        for val in sorted(self.candidates[row][col]):
            if self._is_valid(row, col, val):
                # Assign
                self.puzzle[row][col] = val
                # Save current candidates for forward checking
                old_candidates = copy.deepcopy(self.candidates)
                # Update candidates (forward checking)
                if self._update_candidates(row, col, val):
                    if self._backtrack():
                        return True
                # Restore
                self.puzzle[row][col] = 0
                self.candidates = old_candidates
        return False

    def _is_valid(self, row, col, val):
        """Check if placing val at (row, col) is valid given current puzzle."""
        # row
        if val in self.puzzle[row]:
            return False
        # column
        for i in range(self.size):
            if self.puzzle[i][col] == val:
                return False
        # box
        box_r = (row // self.box_size) * self.box_size
        box_c = (col // self.box_size) * self.box_size
        for i in range(box_r, box_r + self.box_size):
            if val in self.puzzle[i][box_c:box_c + self.box_size]:
                return False
        return True

    def _update_candidates(self, row, col, val):
        """Remove val from candidates of affected cells. Returns False if any cell becomes empty."""
        # Remove from row
        for j in range(self.size):
            if self.puzzle[row][j] == 0 and val in self.candidates[row][j]:
                self.candidates[row][j].remove(val)
                if not self.candidates[row][j]:
                    return False
        # Remove from column
        for i in range(self.size):
            if self.puzzle[i][col] == 0 and val in self.candidates[i][col]:
                self.candidates[i][col].remove(val)
                if not self.candidates[i][col]:
                    return False
        # Remove from box
        box_r = (row // self.box_size) * self.box_size
        box_c = (col // self.box_size) * self.box_size
        for i in range(box_r, box_r + self.box_size):
            for j in range(box_c, box_c + self.box_size):
                if self.puzzle[i][j] == 0 and val in self.candidates[i][j]:
                    self.candidates[i][j].remove(val)
                    if not self.candidates[i][j]:
                        return False
        return True


# ======================================================
# Part 2: Sudoku Generator with Difficulty Control
# ======================================================

class SudokuGenerator:
    def __init__(self):
        self.solver = None

    def generate_full(self):
        """Generate a full solved Sudoku grid using a random backtracking solver."""
        # Start with empty grid
        puzzle = [[0]*9 for _ in range(9)]
        self.solver = SudokuSolver(puzzle)
        # Fill randomly: we can do a simple fill with backtracking that randomizes order
        # But easier: use a solver that randomizes candidate order
        self._random_fill(puzzle)
        return puzzle

    def _random_fill(self, puzzle):
        """Fill the puzzle randomly using backtracking with random candidate order."""
        # Find first empty cell
        for i in range(9):
            for j in range(9):
                if puzzle[i][j] == 0:
                    candidates = self._get_random_candidates(puzzle, i, j)
                    random.shuffle(candidates)
                    for val in candidates:
                        if self._is_valid_placement(puzzle, i, j, val):
                            puzzle[i][j] = val
                            if self._random_fill(puzzle):
                                return True
                            puzzle[i][j] = 0
                    return False
        return True

    def _get_random_candidates(self, puzzle, row, col):
        used = set()
        used.update(puzzle[row])
        used.update(puzzle[i][col] for i in range(9))
        br, bc = row//3*3, col//3*3
        for i in range(br, br+3):
            used.update(puzzle[i][bc:bc+3])
        return [x for x in range(1,10) if x not in used]

    def _is_valid_placement(self, puzzle, row, col, val):
        # Simplified check for validity during generation
        if val in puzzle[row]:
            return False
        for i in range(9):
            if puzzle[i][col] == val:
                return False
        br, bc = row//3*3, col//3*3
        for i in range(br, br+3):
            for j in range(bc, bc+3):
                if puzzle[i][j] == val:
                    return False
        return True

    def remove_cells(self, puzzle, difficulty):
        """Remove cells from a full puzzle to create a puzzle of given difficulty.
        Difficulty: 'easy', 'medium', 'hard' -> number of removed cells.
        Returns a puzzle with zeros for removed cells.
        """
        removed_counts = {'easy': 40, 'medium': 50, 'hard': 60}
        remove = removed_counts[difficulty]
        puzzle = [row[:] for row in puzzle]
        cells = [(i,j) for i in range(9) for j in range(9)]
        random.shuffle(cells)
        removed = 0
        for i,j in cells:
            if removed >= remove:
                break
            # Temporarily remove
            backup = puzzle[i][j]
            puzzle[i][j] = 0
            # Check uniqueness of solution (optional)
            if self._has_unique_solution(puzzle):
                removed += 1
            else:
                puzzle[i][j] = backup
        return puzzle

    def _has_unique_solution(self, puzzle):
        """Check if puzzle has exactly one solution by attempting to find two solutions."""
        solver = SudokuSolver(puzzle)
        # Try to find first solution
        if not solver.solve():
            return False
        
        # Save the first solution
        first_solution = [row[:] for row in solver.puzzle]
        
        # Try to find a second solution by modifying the search
        # Create a new solver and count solutions (limit to 2 for efficiency)
        solution_count = self._count_solutions(puzzle, limit=2)
        return solution_count == 1

    def _count_solutions(self, puzzle, limit=2):
        """Count the number of solutions in a puzzle (up to limit for efficiency)."""
        solver = SudokuSolver(puzzle)
        solver._init_candidates()
        count = [0]  # Use list to allow modification in nested function
        
        def backtrack_and_count():
            if count[0] >= limit:
                return False
            # Find cell with fewest candidates (MRV heuristic)
            min_cell = None
            min_candidates = float('inf')
            for i in range(9):
                for j in range(9):
                    if solver.puzzle[i][j] == 0:
                        cand_count = len(solver.candidates[i][j])
                        if cand_count < min_candidates:
                            min_candidates = cand_count
                            min_cell = (i, j)
                            if min_candidates == 1:
                                break
                if min_candidates == 1:
                    break
            
            if min_cell is None:
                count[0] += 1
                return False  # Continue search for other solutions
            
            row, col = min_cell
            for val in sorted(solver.candidates[row][col]):
                if solver._is_valid(row, col, val):
                    solver.puzzle[row][col] = val
                    old_candidates = copy.deepcopy(solver.candidates)
                    if solver._update_candidates(row, col, val):
                        backtrack_and_count()
                    solver.puzzle[row][col] = 0
                    solver.candidates = old_candidates
                    if count[0] >= limit:
                        return False
            return False
        
        backtrack_and_count()
        return count[0]

    def generate_puzzle(self, difficulty='medium'):
        """Generate a puzzle of specified difficulty."""
        full = self.generate_full()
        puzzle = self.remove_cells(full, difficulty)
        return puzzle


# ======================================================
# Part 3: Machine Learning for Difficulty Prediction
# ======================================================

class DifficultyPredictor:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)

    def extract_features(self, puzzle):
        """Extract features from a puzzle for difficulty prediction.
        Features:
        - number of given cells
        - number of empty cells
        - average candidates per empty cell
        - number of cells with only one candidate
        - number of cells with exactly two candidates
        - etc.
        """
        features = []
        empty_cells = 0
        candidate_counts = []
        solver = SudokuSolver(puzzle)
        solver._init_candidates()
        for i in range(9):
            for j in range(9):
                if puzzle[i][j] == 0:
                    empty_cells += 1
                    cand_count = len(solver.candidates[i][j])
                    candidate_counts.append(cand_count)
        avg_candidates = sum(candidate_counts)/empty_cells if empty_cells>0 else 0
        single_candidates = sum(1 for c in candidate_counts if c==1)
        two_candidates = sum(1 for c in candidate_counts if c==2)
        features = [empty_cells, avg_candidates, single_candidates, two_candidates]
        return features

    def train(self, puzzles, difficulties):
        """Train the model on a list of puzzles and their difficulty labels."""
        X = [self.extract_features(p) for p in puzzles]
        y = difficulties
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        print(f"Model accuracy on test set: {acc:.2f}")
        return acc

    def predict(self, puzzle):
        """Predict difficulty of a given puzzle."""
        features = self.extract_features(puzzle)
        return self.model.predict([features])[0]

    def save(self, filename="difficulty_model.pkl"):
        joblib.dump(self.model, filename)

    def load(self, filename="difficulty_model.pkl"):
        self.model = joblib.load(filename)


# ======================================================
# Part 4: Helper Functions & Example Usage
# ======================================================

def print_puzzle(puzzle, title="Sudoku"):
    print(f"\n{title}:")
    for i, row in enumerate(puzzle):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        row_str = ""
        for j, val in enumerate(row):
            if j % 3 == 0 and j != 0:
                row_str += "| "
            row_str += (str(val) if val != 0 else ".") + " "
        print(row_str)

def generate_training_data(num_samples=1000):
    """Generate synthetic training data for difficulty predictor."""
    generator = SudokuGenerator()
    difficulties = ['easy', 'medium', 'hard']
    puzzles = []
    labels = []
    for _ in range(num_samples):
        diff = random.choice(difficulties)
        puzzle = generator.generate_puzzle(diff)
        puzzles.append(puzzle)
        labels.append(diff)
    return puzzles, labels

def main():
    # Example 1: Solve a given puzzle
    print("=== Sudoku Solver Demo ===")
    puzzle = [
        [5,3,0,0,7,0,0,0,0],
        [6,0,0,1,9,5,0,0,0],
        [0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],
        [4,0,0,8,0,3,0,0,1],
        [7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],
        [0,0,0,4,1,9,0,0,5],
        [0,0,0,0,8,0,0,7,9]
    ]
    print_puzzle(puzzle, "Input Puzzle")
    solver = SudokuSolver(puzzle)
    if solver.solve():
        print_puzzle(solver.puzzle, "Solved Puzzle")
    else:
        print("No solution found.")

    # Example 2: Generate a puzzle
    print("\n=== Sudoku Generator Demo ===")
    generator = SudokuGenerator()
    for diff in ['easy', 'medium', 'hard']:
        puzzle = generator.generate_puzzle(diff)
        print_puzzle(puzzle, f"Generated {diff} puzzle")

    # Example 3: Train ML difficulty predictor
    print("\n=== Training Difficulty Predictor ===")
    puzzles, labels = generate_training_data(num_samples=200)  # small for demo
    predictor = DifficultyPredictor()
    predictor.train(puzzles, labels)
    # Test on a new puzzle
    test_puzzle = generator.generate_puzzle('medium')
    pred = predictor.predict(test_puzzle)
    print_puzzle(test_puzzle, "Test Puzzle")
    print(f"Predicted difficulty: {pred}")

if __name__ == "__main__":
    main()