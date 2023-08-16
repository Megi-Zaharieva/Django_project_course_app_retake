
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from base_app.forms import UserForm, UserProfileInfoForm
from base_app.models import UserProfileInfo
from teacher_app.forms import StudentProfileInfoForm, ProfileDetailsTeacherForm


def index(request):
    if not request.user.is_anonymous:
        profile = User.objects.get(pk=request.user.pk)

        context = {
            'profile': profile,
        }
        return render(request, 'basic_app/index.html', context)
    else:
        return render(request, 'basic_app/index.html')


class UserRegisterView(View):

    def get(self, request):
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'basic_app/registration.html', context)

    def post(self, request):

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            user = authenticate(username=user_form.cleaned_data['username'],
                                password=user_form.cleaned_data['password'])
            login(request, user)


            context = {
                'user_form': user_form,
                'profile_form': profile_form,
            }
            return render(request, 'basic_app/index.html', context)

        else:
            context = {'user_form': user_form,
                       'profile_form': profile_form,
                       }
            return render(request, 'basic_app/registration.html', context)


class UserLoginView(View):
    def get(self, request):
        return render(request, 'basic_app/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['username'] = username
            return redirect('base_app:index')
        else:
            context = {
                'error': 'Invalid User/Password!'
            }
            return render(request, 'basic_app/login.html', context)


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        request.session.clear()
        return redirect('base_app:index')


@login_required
def profile_details(request):
    user = request.user
    user_profile = UserProfileInfo.objects.get(user=user)
    user_type = user_profile.type

    if request.method == 'POST':
        if user_type == "Student":
            user_form = UserForm(request.POST, instance=user)
            profile_form = StudentProfileInfoForm(request.POST, request.FILES, instance=user_profile)
        else:
            user_form = UserForm(request.POST, instance=user)
            profile_form = ProfileDetailsTeacherForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()

            profile_form.save()
            update_session_auth_hash(request, user)
            return redirect('base_app:index')
    else:
        user_form = UserForm(instance=user)
        if user_type == "Student":
            profile_form = StudentProfileInfoForm(instance=user_profile)
        else:
            profile_form = ProfileDetailsTeacherForm(instance=user_profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_type': user_type,
    }
    return render(request, 'basic_app/profile_details.html', context)


def contacts_view(request):
    return render(request, 'basic_app/contacts.html')


def custom_page_not_found(request, *args, **kwargs):
    return render(request, 'basic_app/404.html')