import pandas as pd
from django.shortcuts import render
from .forms import StudentInputForm
from .models import StudentGrade
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

def predict_grade(request):
    prediction = None

    if request.method == "POST":
        form = StudentInputForm(request.POST)
        if form.is_valid():
            # Save student data (optional)
            StudentGrade.objects.create(
                name=form.cleaned_data['name'],
                attendance=form.cleaned_data['attendance'],
                homework=form.cleaned_data['homework'],
                test_score=form.cleaned_data['test_score'],
                final_grade=0  # placeholder
            )

            # Load all data from DB
            qs = StudentGrade.objects.all().values("attendance", "homework", "test_score", "final_grade")
            df = pd.DataFrame(list(qs))

            # Features and target
            X = df[["attendance", "homework", "test_score"]]
            y = df["final_grade"]

            # Train model
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
            model = LinearRegression().fit(X_train, y_train)

            # Predict for new student
            new_student = pd.DataFrame([[
                form.cleaned_data['attendance'],
                form.cleaned_data['homework'],
                form.cleaned_data['test_score']
            ]], columns=["attendance", "homework", "test_score"])

            prediction = model.predict(new_student)[0]

    else:
        form = StudentInputForm()

    return render(request, "grades/predict.html", {"form": form, "prediction": prediction})
