
from django.shortcuts import render
from django.views import View
from course_app.models import CreateCourse
from search_app.forms import SearchForm
from search_app.models import SearchModel


class SearchView(View):
    template_name = 'basic_app/comments/search_results.html'

    def get(self, request):
        form = SearchForm()

        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            search_text = form.cleaned_data['search_text']
            SearchModel.objects.create(search_text=search_text)
            courses_ls = CreateCourse.objects.filter(title__icontains=search_text)

            context = {
                'form': form,
                'courses_ls': courses_ls,
                'search_button_clicked': True
            }
            return render(request, self.template_name, context)

        context = {
            'form': form,
            'search_button_clicked': False
        }
        return render(request, self.template_name, context)
