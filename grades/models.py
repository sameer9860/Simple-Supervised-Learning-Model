from django.db import models

class StudentGrade(models.Model):
    attendance = models.IntegerField()
    homework = models.IntegerField()
    test_score = models.IntegerField()
    final_grade = models.IntegerField()

    def __str__(self):
        return f"Student {self.id} - Grade {self.final_grade}"
