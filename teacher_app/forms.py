
from django import forms
from base_app.models import UserProfileInfo
from base_app.validators import validate_profile_pic, FileExtensionValidator, MaxFileSizeValidator, \
    description_validator, user_comments_validator, review_text_validator
from teacher_app.models import Comments, Review


class StudentProfileInfoForm(forms.ModelForm):
    profile_pic = forms.ImageField(validators=[validate_profile_pic], required=False)

    class Meta():
        model = UserProfileInfo
        fields = ['profile_pic', 'type']
        widgets = {
            'type': forms.TextInput(attrs={'readonly': 'readonly'}),
        }


class ProfileDetailsTeacherForm(forms.ModelForm):
    profile_pic = forms.ImageField(validators=[validate_profile_pic], required=False)
    file = forms.FileField(validators=[FileExtensionValidator(), MaxFileSizeValidator(5 * 1024 * 1024)], required=False)
    description = forms.CharField(validators=[description_validator], required=False)

    class Meta:
        model = UserProfileInfo
        fields = ['profile_pic', 'description', 'type', 'file']
        widgets = {
            'type': forms.TextInput(attrs={'readonly': 'readonly'}),
        }


class CommentsForm(forms.ModelForm):
    user_comments = forms.CharField(validators=[user_comments_validator])

    class Meta:
        model = Comments
        fields = ['user_comments']


class ReviewForm(forms.ModelForm):
    review_text = forms.CharField(validators=[review_text_validator], required=False)

    class Meta:
        model = Review
        fields = ['review_text', 'rating']





