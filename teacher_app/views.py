from django.urls import reverse
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView
from base_app.models import UserProfileInfo
from teacher_app.forms import CommentsForm, ReviewForm
from teacher_app.models import CreateCourse, Comments, Review
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.db.models import Avg


class TeachersHomeView(TemplateView):
    template_name = 'basic_app/teachers/home.html'


class TeacherCoursesView(View):
    def get(self, request):
        user = request.user
        courses_list = CreateCourse.objects.filter(user=user)

        context = {
            'courses_list': courses_list
        }
        return render(request, 'basic_app/teachers/course_list.html', context)


class ListAllTeachersView(View):
    def get(self, request):
        teacher_profiles = UserProfileInfo.objects.filter(type='Teacher', user__is_active=True, admin_approved='Yes')
        teacher_user_ids = [profile.user.id for profile in teacher_profiles]
        teachers_list = User.objects.filter(id__in=teacher_user_ids)

        url = reverse('teacher_app:teacher_courses_list', kwargs={'teacher_id': teachers_list[0].id})
        print("Generated URL:", url)  # Check the printed URL in your console

        context = {
            'teachers_list': teachers_list,
            'teacher_profiles': teacher_profiles,
        }
        return render(request, 'basic_app/students/teachers_list.html', context)


def TeacherCoursesAndDetailsView(request, teacher_id):
    teacher = get_object_or_404(User, id=teacher_id)
    teacher_profile = get_object_or_404(UserProfileInfo, user=teacher)
    courses_list = CreateCourse.objects.filter(user=teacher)

    for course in courses_list:
        course.average_rating = Review.objects.filter(course=course).aggregate(Avg('rating'))['rating__avg']

    context = {
        'teacher': teacher,
        'teacher_profile': teacher_profile,
        'courses_list': courses_list
    }
    return render(request, 'basic_app/teachers/course_list.html', context)


def AddEditComment(request, course_id, comment_id=None):
    user = request.user
    course = get_object_or_404(CreateCourse, id=course_id)

    if comment_id:
        comment = get_object_or_404(Comments, id=comment_id)
    else:
        comment = None

    if request.method == 'POST':
        form = CommentsForm(request.POST, instance=comment)

        if form.is_valid():
            user_comment = form.save(commit=False)
            user_comment.course = course
            user_comment.user = user
            user_comment.save()

            return redirect('course_app:course_details', course_id=course_id)
    else:
        form = CommentsForm(instance=comment)

    context = {
        'form': form,
        'course': course,
        'comment': comment,
    }
    return render(request, 'basic_app/comments/add_edit_comment.html', context)


class DeleteCommentView(UserPassesTestMixin, View):
    template_name = 'basic_app/comments/delete_comment.html'

    def test_func(self):
        comment_id = self.kwargs['comment_id']
        comment = get_object_or_404(Comments, id=comment_id)
        return self.request.user == comment.user or self.request.user.is_superuser or self.request.user.is_staff

    def post(self, request, course_id, comment_id):
        comment = get_object_or_404(Comments, id=comment_id, course_id=course_id)

        if self.test_func():
            comment.delete()
            return redirect('course_app:course_details', course_id=course_id)
        else:
            return HttpResponseForbidden("You are not allowed to delete this comment.")

    def get(self, request, course_id, comment_id):
        if self.test_func():
            course = get_object_or_404(CreateCourse, id=course_id)
            context = {
                'course': course,
            }
            return render(request, self.template_name, context)
        else:
            return HttpResponseForbidden("You are not allowed to delete this comment.")


class AddReviewView(View):
    template_name = 'basic_app/comments/add_review.html'

    def get(self, request, course_id):
        form = ReviewForm()

        context = {
            'form': form,
            'course_id': course_id
        }
        return render(request, self.template_name, context)

    def post(self, request, course_id):
        form = ReviewForm(request.POST)
        course = get_object_or_404(CreateCourse, id=course_id)
        existing_review = Review.objects.filter(course=course, user=request.user).first()
        if existing_review:
            return redirect('teacher_app:view_reviews', course_id=course_id)

        if form.is_valid():
            review = form.save(commit=False)
            review.course = course
            review.user = request.user
            review.save()
            return redirect('teacher_app:view_reviews', course_id=course_id)

        context = {
            'form': form,
            'course_id': course_id
        }
        return render(request, self.template_name, context)


class ViewReviews(View):
    template_name = 'basic_app/comments/view_reviews.html'

    def get(self, request, course_id):
        reviews = Review.objects.filter(course_id=course_id)
        user_has_review = Review.objects.filter(course_id=course_id, user=request.user).exists()

        if user_has_review:
            messages.error(request, 'Review already added.')

        context = {
            'reviews': reviews,
            'course_id': course_id,
            'user_has_review': user_has_review
        }
        return render(request, self.template_name, context)
