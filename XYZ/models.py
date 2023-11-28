from django.db import models
from django import forms
# Create your models here.

class BasicModel(models.Model):
    project_name = models.CharField(max_length=100)
    project_description = models.TextField(blank=True)
    client = models.CharField(max_length=255)
    contractor = models.CharField(max_length=255)

    def __str__(self):
        return self.project_name


class InputModel(models.Model):
    basic_model = models.ForeignKey(BasicModel, on_delete=models.CASCADE)
    maximum_x = models.DecimalField(max_digits=20, decimal_places=6)
    minimum_x = models.DecimalField(max_digits=20, decimal_places=6)
    maximum_y = models.DecimalField(max_digits=20, decimal_places=6)
    minimum_y = models.DecimalField(max_digits=20, decimal_places=6)
    maximum_z = models.DecimalField(max_digits=20, decimal_places=6)
    minimum_z = models.DecimalField(max_digits=20, decimal_places=6)

    def __str__(self):
        return self.basic_model.project_name
    

# form class

class BasicForm(forms.ModelForm):

    class Meta:
        model = BasicModel
        fields = "__all__"


class InputForm(forms.ModelForm):

    class Meta:
        model = InputModel
        exclude = ('basic_model',)


    



