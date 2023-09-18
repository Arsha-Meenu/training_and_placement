from django.contrib import admin
from .models import User,Job,Subject,Training,JobSelectedUser

admin.site.register(User)
admin.site.register(Job)
admin.site.register(Training)
admin.site.register(Subject)
admin.site.register(JobSelectedUser)