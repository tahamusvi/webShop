from django.contrib import admin
from .models import UserVisit

class UserVisitAdmin(admin.ModelAdmin):
    list_display = ('user_identifier', 'http_method', 'request_url', 'created_at') 
    list_filter = ('http_method',)  
    search_fields = ('user_identifier', 'request_url') 
    readonly_fields = ('user_identifier', 'http_method', 'request_url', 'user_agent', 'created_at') 
    date_hierarchy = 'created_at'  

admin.site.register(UserVisit, UserVisitAdmin)