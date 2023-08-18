from django import forms
from assignment_app.models import Assignment
from base_app.validators import description_validator, title_validator


class AssignmentForm(forms.ModelForm):
    description = forms.CharField(validators=[description_validator])
    title = forms.CharField(validators=[title_validator])

    class Meta:
        model = Assignment
        fields = ['title', 'description']
