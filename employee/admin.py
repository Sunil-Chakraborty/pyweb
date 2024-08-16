from django.contrib import admin
from .models import Employee

# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('eid', 'ename', 'eemail','econtact','prof_image')


admin.site.register(Employee,EmployeeAdmin)