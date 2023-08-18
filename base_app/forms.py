
from django import forms
from django.contrib.auth.models import User
from base_app.models import UserProfileInfo
from base_app.validators import password_validation, password_validators, PasswordInfo, UsernameValidator, \
    username_validation, email_validation, first_name_validator, last_name_validator, validate_profile_pic


class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(),
                               validators=[password_validation, password_validators],
                               help_text=PasswordInfo().get_help_text())

    username = forms.CharField(help_text=UsernameValidator().get_help_text(),
                               validators=[username_validation])

    email = forms.EmailField(validators=[email_validation])
    first_name = forms.CharField(validators=[first_name_validator], required=False)
    last_name = forms.CharField(validators=[last_name_validator], required=False)

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''

        for field_name in self.fields:
            field = self.fields[field_name]
            placeholder = field.label if field.label else field_name.replace('_', ' ').capitalize()
            field.widget.attrs['placeholder'] = placeholder
            field.widget.attrs['class'] = 'form-control'
            field.label = ''

    class Meta():
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def as_div(self):
        return self._html_output(
            normal_row='<div class="form__row"><div class="form__controls">%(label)s%(field)s%(help_text)s</div></div>',
            error_row='%s',
            row_ender='</div>',
            help_text_html='<p class="form__row--help-text">%s</p>',
            errors_on_separate_row=True,)


class UserProfileInfoForm(forms.ModelForm):
    profile_pic = forms.ImageField(validators=[validate_profile_pic], required=False)

    def __init__(self, *args, **kwargs):
        super(UserProfileInfoForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''

        for field_name in self.fields:
            field = self.fields[field_name]
            placeholder = field.label if field.label else field_name.replace('_', ' ').capitalize()
            field.widget.attrs['placeholder'] = placeholder
            field.widget.attrs['class'] = 'form-control'
            field.label = False

        if 'type' in self.fields:
            self.fields['type'].choices = UserProfileInfo.CHOICES
            self.fields['type'].choices.insert(0, ('', 'Select a role'))
            self.fields['type'].initial = ''

    def as_div(self):
         return self._html_output(
            normal_row='<div class="form__row"><div class="form__controls">%(label)s%(field)s%(help_text)s</div></div>',
            error_row='%s',
            row_ender='</div>',
            help_text_html='<p class="form__row--help-text">%s</p>',
            errors_on_separate_row=True,
        )

    class Meta():
        model = UserProfileInfo
        fields = ['profile_pic', 'type']
