from django.contrib import admin
from .models import Job, UserProfile, Application, JobCategory

class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_employer', 'phone_number', 'created_at')
    list_filter = ('is_employer', 'created_at')
    search_fields = ('user__username', 'phone_number')
    readonly_fields = ('created_at', 'updated_at')

class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'job_type', 'experience_level', 'posted_by', 'posted_on', 'is_active')
    list_filter = ('job_type', 'experience_level', 'is_active', 'posted_on')
    search_fields = ('title', 'company', 'location')
    readonly_fields = ('posted_on', 'views_count')
    raw_id_fields = ('posted_by', 'category')
    date_hierarchy = 'posted_on'

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'status', 'applied_on')
    list_filter = ('status', 'applied_on')
    search_fields = ('job__title', 'applicant__username')
    readonly_fields = ('applied_on', 'updated_on')
    raw_id_fields = ('job', 'applicant')

admin.site.register(JobCategory, JobCategoryAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Application, ApplicationAdmin)
