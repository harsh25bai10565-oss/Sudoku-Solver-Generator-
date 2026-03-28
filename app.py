from flask import Flask, render_template, request, jsonify
import sudoku
import numpy as np
import random
import json
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

app = Flask(__name__)

# Load or train ML model once at startup
MODEL_PATH = 'difficulty_model.pkl'
predictor = sudoku.DifficultyPredictor()

if os.path.exists(MODEL_PATH):
    predictor.load(MODEL_PATH)
else:
    # Generate training data and train model (this may take a moment)
    print("Training difficulty predictor...")
    puzzles, labels = sudoku.generate_training_data(num_samples=500)
    predictor.train(puzzles, labels)
    predictor.save(MODEL_PATH)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    data = request.get_json()
    puzzle = data.get('puzzle')
    if not puzzle:
        return jsonify({'error': 'No puzzle provided'}), 400
    solver = sudoku.SudokuSolver(puzzle)
    if solver.solve():
        return jsonify({'solution': solver.puzzle})
    else:
        return jsonify({'error': 'No solution found'}), 400

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    difficulty = data.get('difficulty', 'medium')
    gen = sudoku.SudokuGenerator()
    puzzle = gen.generate_puzzle(difficulty)
    return jsonify({'puzzle': puzzle})

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    puzzle = data.get('puzzle')
    if not puzzle:
        return jsonify({'error': 'No puzzle provided'}), 400
    pred = predictor.predict(puzzle)
    return jsonify({'difficulty': pred})

if __name__ == '__main__':
    app.run(debug=True)