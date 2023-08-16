from django.contrib.auth.decorators import login_required
from django.urls import path
from assignment_app.views import CreateAssignmentView, ViewAssignmentsView, DeleteAssignmentView

app_name = 'assignment_app'

urlpatterns = [
    path('create/<int:course_id>/', login_required(CreateAssignmentView.as_view()), name='create_assignment'),
    path('view/<int:course_id>/', login_required(ViewAssignmentsView.as_view()), name='view_assignments'),
    path('delete/<int:course_id>/<int:assignment_id>/', login_required(DeleteAssignmentView.as_view()), name='delete_assignment'),
]
