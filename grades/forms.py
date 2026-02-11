from django import forms

class StudentInputForm(forms.Form):
    name = forms.CharField(max_length=100)
    attendance = forms.IntegerField()
    homework = forms.IntegerField()
    test_score = forms.IntegerField()
