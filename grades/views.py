import pandas as pd
from django.shortcuts import render
from .forms import StudentInputForm
from .models import StudentGrade
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

def predict_grade(request):
    prediction = None

    if request.method == "POST":
        form = StudentInputForm(request.POST)
        if form.is_valid():
            # Check if student already exists with same data
            existing_student = StudentGrade.objects.filter(
                name=form.cleaned_data['name'],
                attendance=form.cleaned_data['attendance'],
                homework=form.cleaned_data['homework'],
                test_score=form.cleaned_data['test_score']
            ).first()

            if existing_student:
                prediction = existing_student.final_grade
            else:
                # Load only students with real grades for training
                qs = StudentGrade.objects.exclude(final_grade=0).values(
                    "attendance", "homework", "test_score", "final_grade"
                )
                df = pd.DataFrame(list(qs))

                if not df.empty:
                    # Train model(Supervised Training Model)
                    X = df[["attendance", "homework", "test_score"]]
                    y = df["final_grade"]
                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
                    model = RandomForestRegressor(n_estimators=100, random_state=42).fit(X_train, y_train)

                    # Predict new student
                    new_student = pd.DataFrame([[
                        form.cleaned_data['attendance'],
                        form.cleaned_data['homework'],
                        form.cleaned_data['test_score']
                    ]], columns=["attendance", "homework", "test_score"])

                    prediction = model.predict(new_student)[0]
                    prediction = max(0, min(100, round(prediction)))  # Cap between 0-100 and round

                    # Save student with predicted grade
                    StudentGrade.objects.create(
                        name=form.cleaned_data['name'],
                        attendance=form.cleaned_data['attendance'],
                        homework=form.cleaned_data['homework'],
                        test_score=form.cleaned_data['test_score'],
                        final_grade=prediction
                    )
    else:
        form = StudentInputForm()

    # Get all students for dashboard
    students = StudentGrade.objects.all()

    return render(request, "grades/predict.html", {
        "form": form,
        "prediction": prediction,
        "students": students
    })
