# AI Test Outcome Prediction

## Problem Statement
Traditional test automation determines failure only after assertions fail.
This project predicts test outcomes early using runtime and performance signals.

## Features Used
- API response time
- Page reload frequency
- Test execution duration

## Tech Stack
- Python
- Playwright
- Pytest
- NumPy, Pandas
- Scikit-learn

## Workflow
1. Run Playwright tests and collect runtime metrics
2. Store metrics as historical data
3. Train ML model to classify PASS vs FAIL
4. Predict outcome for new test runs

## Use Case
- Early detection of unstable tests
- Reduce flaky failures in CI pipelines

## How to Run
1. Install dependencies
   pip install -r requirements.txt

2. Install Playwright browsers
   playwright install

3. Train model
   python src/train_model.py

4. Run prediction
   python src/predict_outcome.py
