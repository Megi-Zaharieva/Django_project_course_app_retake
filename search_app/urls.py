
from django.urls import path
from django.contrib.auth.decorators import login_required
from search_app import views

app_name = 'search_app'

urlpatterns = [

    path('results/', login_required(views.SearchView.as_view()), name='search_results'),
]
