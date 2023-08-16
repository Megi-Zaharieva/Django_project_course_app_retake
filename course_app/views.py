
from django.shortcuts import redirect
from django.views import View
from course_app.forms import AddCourseForm
from teacher_app.models import CreateCourse, Comments, Review
from django.shortcuts import render, get_object_or_404
from django.utils import timezone



class AddCourseView(View):
    def get(self, request):
        form = AddCourseForm()
        context = {
            'form': form
        }
        return render(request, 'basic_app/teachers/add-course.html', context)

    def post(self, request):
        form = AddCourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user
            course.date = timezone.now()

            if 'course_image_url' in request.FILES:
                course.course_image_url = request.FILES['course_image_url']

            course.save()
            return redirect('course_app:my_courses')

        context = {
            'form': form
        }
        return render(request, 'basic_app/teachers/add-course.html', context)


class CourseDetailsView(View):
    template_name = 'basic_app/teachers/course-details.html'

    def get(self, request, course_id):
        form = get_object_or_404(CreateCourse, id=course_id)
        video_url = form.video_url
        video_url_split = video_url.split("=")
        video_id = video_url_split[1]
        video_details = YoutubeVideoUrl(video_id)
        comments_ls = Comments.objects.filter(course_id=course_id).order_by('-id')
        course_id = form.id
        user_has_review = Review.objects.filter(course_id=course_id, user=request.user).exists()

        context = {
            'video_details': video_details,
            'form': form,
            'comments_ls': comments_ls,
            'course_id': course_id,
            'user_has_review': user_has_review,
        }
        return render(request, self.template_name, context)


def YoutubeVideoUrl(video_id):
    embed_url = f"https://www.youtube.com/embed/{video_id}"
    return embed_url


class EditCourseView(View):
    template_name = 'basic_app/teachers/course-edit.html'

    def get(self, request, course_id):

        if request.user.is_superuser or request.user.is_staff:
            course = get_object_or_404(CreateCourse, id=course_id)
        else:
            course = get_object_or_404(CreateCourse, id=course_id, user=request.user)

        form = AddCourseForm(instance=course)
        context = {
            'form': form,
            'course': course
        }
        return render(request, self.template_name, context)

    def post(self, request, course_id):
        if request.user.is_superuser or request.user.is_staff:
            course = get_object_or_404(CreateCourse, id=course_id)
        else:
            course = get_object_or_404(CreateCourse, id=course_id, user=request.user)

        form = AddCourseForm(request.POST, instance=course)
        if form.is_valid():
            course = form.save(commit=False)
            course.date = timezone.now()
            course.save()
            return redirect('course_app:course_details', course_id=course.id)
        context = {
            'form': form,
            'course': course
        }
        return render(request, self.template_name, context)


class DeleteCourseView(View):
    def test_func(self, request, course_id):
        course = get_object_or_404(CreateCourse, id=course_id)
        return self.request.user == course.user or self.request.user.is_superuser or self.request.user.is_staff

    def get(self, request, course_id):
        course = get_object_or_404(CreateCourse, id=course_id)

        context = {
            'course': course
        }
        return render(request, 'basic_app/teachers/course-delete.html', context)

    def post(self, request, course_id):
        course = get_object_or_404(CreateCourse, id=course_id)

        if self.test_func(request, course_id):
            course.delete()
            return redirect('course_app:my_courses')
        else:
            return render(request, 'basic_app/teachers/access_denied.html')