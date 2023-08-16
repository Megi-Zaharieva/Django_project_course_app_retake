from django.contrib.auth.decorators import login_required
from django.urls import path
from base_app import views
from base_app.views import UserRegisterView, UserLoginView, UserLogoutView


app_name = 'base_app'

urlpatterns = [

    path('', views.index, name='index'),
    path('register/', UserRegisterView.as_view(), name='registration'),
    path('user_login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('404/', views.custom_page_not_found, name='error'),
    path('profile/details', login_required(views.profile_details), name='profile_details'),
    path('contacts/', views.contacts_view, name='contacts'),

]
handler404 = 'base_app.views.custom_page_not_found'