# Sudoku Solver & Generator with AI/ML

This project demonstrates classic AI search techniques and machine learning applied to Sudoku puzzles.

## Features

- **AI Solver**: Uses backtracking with **Minimum Remaining Values (MRV)** heuristic and **forward checking** for efficient solving.
- **Generator**: Creates valid Sudoku puzzles with adjustable difficulty (easy/medium/hard).
- **Difficulty Predictor**: Machine learning model (Random Forest) trained to predict puzzle difficulty based on features like number of empty cells, average candidates, etc.

## Installation

1. Clone this repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask application:
   ```bash
   python app.py
   ```
4. Open your browser and navigate to `http://localhost:5000`

## Usage

### Solve a Puzzle
- **Manually enter a puzzle**: Fill in the 9x9 grid with numbers 1-9 (use 0 or leave empty for unknown cells)
- **Click "Solve"**: The solver will find the solution using backtracking with MRV heuristic and forward checking
- **View the solution**: Solved cells will be filled in automatically

### Generate a Puzzle
- **Select difficulty**: Choose from Easy (40 clues), Medium (50 clues), or Hard (60 clues)
- **Click "Generate"**: A new puzzle will be created with the selected difficulty level
- **Start solving**: Use the Solve feature or solve manually

### Predict Difficulty
- **Enter or generate a puzzle**
- **Click "Predict Difficulty"**: The ML model will estimate the puzzle's difficulty level

## Project Structure

```
vit/
├── app.py              # Flask web application with API endpoints
├── sudoku.py           # Core Sudoku solver, generator, and ML predictor
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # Web interface
├── static/
│   ├── script.js       # Frontend JavaScript
│   └── style.css       # Styling
└── README.md           # This file
```

## Technical Details

### AI Solver Algorithm
- **Backtracking Search**: Explores possible values for empty cells
- **Minimum Remaining Values (MRV) Heuristic**: Selects cells with fewest candidates first for efficiency
- **Forward Checking**: Prunes candidate values to detect failures early

### Machine Learning Predictor
- **Algorithm**: Random Forest Classifier with 100 estimators
- **Features**: Number of empty cells, average candidates per cell, cells with 1-2 candidates
- **Training Data**: Generated synthetically from puzzles of known difficulty

### Generator Strategy
- **Full Grid Generation**: Uses randomized backtracking to create valid complete grids
- **Cell Removal**: Progressively removes cells while maintaining solution uniqueness