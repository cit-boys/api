from django.contrib import admin

from src.mysalary.models import Level, Certificate, Company, Contribution

# Register your models here.

admin.site.register(Level)
admin.site.register(Certificate)
admin.site.register(Company)
admin.site.register(Contribution)
