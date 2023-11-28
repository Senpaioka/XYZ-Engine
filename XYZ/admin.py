from django.contrib import admin
from XYZ.models import BasicModel, InputModel

# Register your models here.

class BasicModelAdmin(admin.ModelAdmin):
    list_display = ["project_name", "client", "contractor"]

class InputModelAdmin(admin.ModelAdmin):
    list_display = ["basic_model", "maximum_x", "minimum_x", "maximum_y", "minimum_y", "maximum_z","minimum_z"]
    

admin.site.register(BasicModel, BasicModelAdmin)
admin.site.register(InputModel, InputModelAdmin)
