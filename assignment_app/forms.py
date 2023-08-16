from django import forms
from assignment_app.models import Assignment


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description']
