from django import forms
from base_app.validators import description_validator, title_validator, validate_profile_pic
from course_app.models import CreateCourse


class AddCourseForm(forms.ModelForm):
    description = forms.CharField(validators=[description_validator], required=False)
    title = forms.CharField(validators=[title_validator], required=True)
    course_image = forms.ImageField(validators=[validate_profile_pic], required=False)

    def __init__(self, *args, **kwargs):
        super(AddCourseForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''

        for field_name in self.fields:
            field = self.fields[field_name]
            placeholder = field.label if field.label else field_name.capitalize()
            field.widget.attrs['placeholder'] = placeholder
            field.widget.attrs['class'] = 'form-control'
            field.label = False

    def as_div(self):
        return self._html_output(
            normal_row='<div class="form__row"><div class="form__controls">%(label)s%(field)s%(help_text)s</div></div>',
            error_row='%s',
            row_ender='</div>',
            help_text_html='<p class="form__row--help-text">%s</p>',
            errors_on_separate_row=True,
        )

    class Meta:
        model = CreateCourse
        fields = ['title', 'video_url', 'course_image', 'type', 'description']
