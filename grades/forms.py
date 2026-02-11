from django import forms

class StudentInputForm(forms.Form):
    name = forms.CharField(max_length=100)
    attendance = forms.IntegerField(min_value=0, max_value=100)
    homework = forms.IntegerField(min_value=0, max_value=100)
    test_score = forms.IntegerField(min_value=0, max_value=99)
