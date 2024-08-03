from django.contrib import admin
from django.urls import path,include
from exelapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.upload_file, name='upload_file'),
    path('transform/', views.transform_file, name='transform_file'),
    path('download/', views.download_file, name='download_file'),
    path('', include('exelapp.urls')),
]
