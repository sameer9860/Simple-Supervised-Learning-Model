import os
import django
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SuperLearning.settings")
django.setup()

from grades.models import StudentGrade

# Load data from SQLite
qs = StudentGrade.objects.all().values("id", "name", "attendance", "homework", "test_score", "final_grade")
df = pd.DataFrame(list(qs))

# Features and target
X = df[["attendance", "homework", "test_score"]]
y = df["final_grade"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train models(Supervised Training Model)
lin_model = LinearRegression().fit(X_train, y_train)
rf_model = RandomForestRegressor(n_estimators=100, random_state=42).fit(X_train, y_train)

# Evaluate
lin_pred = lin_model.predict(X_test)
rf_pred = rf_model.predict(X_test)

print("Linear Regression R2:", r2_score(y_test, lin_pred))
print("Random Forest R2:", r2_score(y_test, rf_pred))

# Predict new student
new_student = pd.DataFrame([[90, 85, 80]], columns=["attendance", "homework", "test_score"])
print("Linear Regression Prediction:", lin_model.predict(new_student))
print("Random Forest Prediction:", rf_model.predict(new_student))
