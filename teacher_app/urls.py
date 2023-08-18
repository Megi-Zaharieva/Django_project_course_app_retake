from django.contrib.auth.decorators import login_required
from django.urls import path
from teacher_app import views
from teacher_app.views import ListAllTeachersView, TeachersHomeView

app_name = 'teacher_app'

urlpatterns = [

    path('teachers_list/', login_required(ListAllTeachersView.as_view()), name='teachers_list'),
    path('teacher/<int:teacher_id>/courses/', login_required(views.TeacherCoursesAndDetailsView),
     name='teacher_courses_list'),
    path('course/<int:course_id>/add_comment/', login_required(views.AddEditComment), name='add_comment'),
    path('course/<int:course_id>/edit_comment/<int:comment_id>/', login_required(views.AddEditComment),
         name='edit_comment'),
    path('course/<int:course_id>/delete_comment/<int:comment_id>/', login_required(views.DeleteCommentView.as_view()),
         name='delete_comment'),
    path('course/<int:course_id>/add_review/', login_required(views.AddReviewView.as_view()), name='add_review'),
    path('view_reviews/<int:course_id>', login_required(views.ViewReviews.as_view()), name='view_reviews'),
    path('teachers/home/', login_required(TeachersHomeView.as_view()), name='teachers_home'),

]
