from django.contrib import admin
from .models import User, Task, Family, QuickTask

# Register your models here.
admin.site.register(User)
admin.site.register(Task)
admin.site.register(Family)
admin.site.register(QuickTask)