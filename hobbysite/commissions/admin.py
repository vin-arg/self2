from django.contrib import admin
from .models import Commission, Job, JobApplication

class JobInLine(admin.TabularInline):
    model = Job

class CommissionAdmin(admin.ModelAdmin):
    model = Commission
    inlines = [JobInLine]

class JobAdmin(admin.ModelAdmin):
    model = Job

class JobApplicationAdmin(admin.ModelAdmin):
    model = JobApplication

admin.site.register(Commission, CommissionAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)