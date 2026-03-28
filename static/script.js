document.addEventListener('DOMContentLoaded', () => {
    const grid = document.getElementById('sudoku-grid');
    const solveBtn = document.getElementById('solve-btn');
    const generateBtn = document.getElementById('generate-btn');
    const predictBtn = document.getElementById('predict-btn');
    const clearBtn = document.getElementById('clear-btn');
    const difficultySelect = document.getElementById('difficulty-select');
    const messageDiv = document.getElementById('message');

    // Create 9x9 grid of input cells
    function createGrid(puzzle = null) {
        grid.innerHTML = '';
        for (let i = 0; i < 9; i++) {
            for (let j = 0; j < 9; j++) {
                const cell = document.createElement('div');
                cell.className = 'sudoku-cell';
                const input = document.createElement('input');
                input.type = 'text';
                input.maxLength = 1;
                input.id = `cell-${i}-${j}`;
                if (puzzle && puzzle[i][j] !== 0) {
                    input.value = puzzle[i][j];
                } else {
                    input.value = '';
                }
                // Restrict input to digits 1-9
                input.addEventListener('input', (e) => {
                    let val = e.target.value;
                    if (val && !/[1-9]/.test(val)) {
                        e.target.value = '';
                    }
                });
                cell.appendChild(input);
                grid.appendChild(cell);
            }
        }
    }

    // Read current puzzle from grid
    function getPuzzle() {
        const puzzle = [];
        for (let i = 0; i < 9; i++) {
            const row = [];
            for (let j = 0; j < 9; j++) {
                const input = document.getElementById(`cell-${i}-${j}`);
                const val = input.value.trim();
                row.push(val ? parseInt(val) : 0);
            }
            puzzle.push(row);
        }
        return puzzle;
    }

    // Set puzzle into grid
    function setPuzzle(puzzle) {
        for (let i = 0; i < 9; i++) {
            for (let j = 0; j < 9; j++) {
                const input = document.getElementById(`cell-${i}-${j}`);
                const val = puzzle[i][j];
                input.value = val !== 0 ? val : '';
            }
        }
    }

    // Show message
    function showMessage(text, type = 'info') {
        messageDiv.textContent = text;
        messageDiv.className = `message ${type}`;
        setTimeout(() => {
            messageDiv.textContent = '';
            messageDiv.className = 'message';
        }, 3000);
    }

    // API calls
    async function solvePuzzle() {
        const puzzle = getPuzzle();
        try {
            const response = await fetch('/solve', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ puzzle })
            });
            const data = await response.json();
            if (response.ok) {
                setPuzzle(data.solution);
                showMessage('Puzzle solved!', 'success');
            } else {
                showMessage(data.error || 'Error solving puzzle', 'error');
            }
        } catch (err) {
            showMessage('Network error', 'error');
        }
    }

    async function generatePuzzle() {
        const difficulty = difficultySelect.value;
        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ difficulty })
            });
            const data = await response.json();
            if (response.ok) {
                setPuzzle(data.puzzle);
                showMessage(`Generated ${difficulty} puzzle`, 'success');
            } else {
                showMessage(data.error || 'Error generating puzzle', 'error');
            }
        } catch (err) {
            showMessage('Network error', 'error');
        }
    }

    async function predictDifficulty() {
        const puzzle = getPuzzle();
        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ puzzle })
            });
            const data = await response.json();
            if (response.ok) {
                showMessage(`Predicted difficulty: ${data.difficulty}`, 'info');
            } else {
                showMessage(data.error || 'Error predicting difficulty', 'error');
            }
        } catch (err) {
            showMessage('Network error', 'error');
        }
    }

    function clearGrid() {
        for (let i = 0; i < 9; i++) {
            for (let j = 0; j < 9; j++) {
                const input = document.getElementById(`cell-${i}-${j}`);
                input.value = '';
            }
        }
        showMessage('Grid cleared', 'info');
    }

    // Initialize empty grid
    createGrid();

    // Event listeners
    solveBtn.addEventListener('click', solvePuzzle);
    generateBtn.addEventListener('click', generatePuzzle);
    predictBtn.addEventListener('click', predictDifficulty);
    clearBtn.addEventListener('click', clearGrid);
});