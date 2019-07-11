from django.contrib import admin
from nbapp1 import models

# Register your models here.
from nbapp1 import models
class StudentStudyRecordAdmin(admin.ModelAdmin):
    list_display =['student','classstudyrecord','record','score']
    list_editable = ['record','score']

admin.site.register(models.UserInfo)
admin.site.register(models.Customer)
admin.site.register(models.Campuses)
admin.site.register(models.ClassList)
admin.site.register(models.ClassStudyRecord)
admin.site.register(models.StudentStudyRecord,StudentStudyRecordAdmin)
admin.site.register(models.Student)











