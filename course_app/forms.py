from django import forms
from base_app.validators import description_validator, title_validator, course_image_url_validator
from course_app.models import CreateCourse


class AddCourseForm(forms.ModelForm):
    description = forms.CharField(validators=[description_validator], required=False)
    title = forms.CharField(validators=[title_validator], required=True)
    course_image_url = forms.CharField(validators=[course_image_url_validator], required=False)

    class Meta:
        model = CreateCourse
        fields = ['title', 'video_url', 'course_image_url', 'type', 'description']

