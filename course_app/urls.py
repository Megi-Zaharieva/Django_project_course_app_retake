from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.urls import path
from course_app.views import AddCourseView, CourseDetailsView, EditCourseView, DeleteCourseView
from teacher_app.views import TeacherCoursesView

app_name = 'course_app'

urlpatterns = [

    path('teachers/add_course/', login_required(AddCourseView.as_view()), name='add_course'),
    path('teachers/my_courses/', login_required(TeacherCoursesView.as_view()), name='my_courses'),
    path('course/details/<int:course_id>/', login_required(CourseDetailsView.as_view()), name='course_details'),
    path('course/edit/<int:course_id>/', login_required(EditCourseView.as_view()), name='edit_course'),
    path('course/delete/<int:course_id>/', login_required(DeleteCourseView.as_view()), name='delete_course'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)