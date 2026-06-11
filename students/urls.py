from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('student/create/', views.StudentCreateView.as_view(), name='student_create'),
]