
from django import forms
from base_app.validators import search_validator


class SearchForm(forms.Form):
    search_text = forms.CharField(label='Search', max_length=255, validators=[search_validator])