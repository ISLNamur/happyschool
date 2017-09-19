from django.contrib import admin
from .models import StudentModel, TeachingModel, ResponsibleModel, AdditionalStudentInfo, ClasseModel, EmailModel, YearModel

admin.site.register(StudentModel)
admin.site.register(TeachingModel)
admin.site.register(ResponsibleModel)
admin.site.register(AdditionalStudentInfo)
admin.site.register(ClasseModel)
admin.site.register(EmailModel)
admin.site.register(YearModel)