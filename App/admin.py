from django.contrib import admin
from .models import *
# Register your models here.
admin.site.site_header = 'Job Portal'

admin.site.register(Job_Seeker)
admin.site.register(Recruiter)


class Job_PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'posted_on', 'upto']
    search_fields = ['user', 'post']

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']
    search_fields = ['name', 'email']


admin.site.register(Job_Post, Job_PostAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(AppliedPost)
    

