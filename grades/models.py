from django.db import models

class StudentGrade(models.Model):
    # Django automatically creates an 'id' primary key field, so you don’t need to define it manually
    name = models.CharField(max_length=100)   # student name
    attendance = models.IntegerField()
    homework = models.IntegerField()
    test_score = models.IntegerField()
    final_grade = models.IntegerField()

    def __str__(self):
        return f"{self.name} - Grade {self.final_grade}"
