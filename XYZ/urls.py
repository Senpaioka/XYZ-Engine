from django.contrib import admin
from django.urls import path
from XYZ import views

app_name='XYZ'

urlpatterns = [
    path('', views.first_form, name='first_form'),
    path('form/', views.second_form, name='second_form'),
    path('csv/', views.csv_form, name='csv_form'),
    path('csv_process/', views.csv_process, name='csv_process'),
    path('final/', views.final_view, name='final_link'),
]
