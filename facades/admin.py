from django.contrib import admin
from .models import FAQ, Cover, FAQGroup, Survey
# Register your models here.

admin.site.register(Cover)
admin.site.register(Survey)
admin.site.register(FAQ)
admin.site.register(FAQGroup)