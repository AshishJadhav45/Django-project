# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('transform/', views.transform_file, name='transform_file'),
    path('download/', views.download_file, name='download_file'),
    path('plot/', views.plot_image, name='plot_image'),  
]
