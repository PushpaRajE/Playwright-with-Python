import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load historical test execution data
data = pd.read_csv("test_data.csv")

# Features (input to AI)
X = data[["execution_time", "code_changes", "failures_last_5_runs"]]

# Label: 1 = high priority, 0 = low priority
y = (data["failures_last_5_runs"] > 1).astype(int)

# Train AI model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save trained model
joblib.dump(model, "priority_model.pkl")

print("✅ AI test prioritization model trained")
