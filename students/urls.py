from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("student/create/", views.StudentCreateView.as_view(), name="student_create"),
    path(
        "student/<int:pk>/delete/",
        views.StudentDeleteView.as_view(),
        name="student_delete",
    ),
    path(
        "student/<int:pk>/update/",
        views.StudentUpdateView.as_view(),
        name="student_update",
    ),
    path("subject/create/", views.SubjectCreateView.as_view(), name="subject_create"),
    path(
        "subject/<int:pk>/update/",
        views.SubjectUpdateView.as_view(),
        name="subject_update",
    ),
    path(
        "subject/<int:pk>/delete/",
        views.SubjectDeleteView.as_view(),
        name="subject_delete",
    ),
]
