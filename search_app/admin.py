
from django.contrib import admin
from search_app.models import SearchModel


class SearchModelAdmin(admin.ModelAdmin):
    list_display = ['search_text', 'created_at']
    list_filter = ['created_at']
    search_fields = ['search_text']
    list_per_page = 10
    ordering = ['-created_at']


admin.site.register(SearchModel, SearchModelAdmin)