from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base_app.urls', namespace='base_app')),
    path('courses/', include('course_app.urls', namespace='course_app')),
    path('search/', include('search_app.urls', namespace='search_app')),
    path('teacher_app/', include('teacher_app.urls', namespace='teacher_app')),
    path('assignment_app/', include('assignment_app.urls', namespace='assignment_app')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

