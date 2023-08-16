from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from assignment_app.forms import AssignmentForm
from assignment_app.models import Assignment
from course_app.models import CreateCourse


class CreateAssignmentView(View):
    template_name = 'basic_app/create_assignment/create-assignment.html'

    def get(self, request, course_id):
        course = get_object_or_404(CreateCourse, id=course_id)
        form = AssignmentForm()
        context = {
            'course': course,
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, course_id):
        course = get_object_or_404(CreateCourse, id=course_id)
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.course = course
            assignment.created_by = request.user
            assignment.save()
            return redirect('assignment_app:view_assignments', course_id=course.id)
        context = {
            'course': course,
            'form': form
        }
        return render(request, self.template_name, context)


class ViewAssignmentsView(View):
    template_name = 'basic_app/create_assignment/view-assignments.html'

    def get(self, request, course_id):
        course = get_object_or_404(CreateCourse, id=course_id)
        assignments = Assignment.objects.filter(course=course)

        context = {
            'course': course,
            'assignments': assignments,
        }
        return render(request, self.template_name, context)


class DeleteAssignmentView(View):
    template_name = 'basic_app/create_assignment/confirm_delete_assignment.html'

    def get(self, request, course_id, assignment_id):
        assignment = get_object_or_404(Assignment, id=assignment_id)
        if assignment.created_by == request.user or request.user.is_staff or request.user.is_superuser:
            context = {
                'assignment': assignment,
                'course_id': course_id
            }
            return render(request, self.template_name, context)
        return redirect('assignment_app:view_assignments', course_id=course_id)

    def post(self, request, course_id, assignment_id):
        assignment = get_object_or_404(Assignment, id=assignment_id)
        if assignment.created_by == request.user or request.user.is_staff or request.user.is_superuser:
            assignment.delete()
        return redirect('assignment_app:view_assignments', course_id=course_id)

