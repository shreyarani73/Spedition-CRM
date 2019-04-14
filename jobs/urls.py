from django.urls import path
from . import views

app_name = "jobs"

urlpatterns = [
    path('view/<int:job_id>/delete-process/<int:process_id>/', views.delete_process, name="delete-process"),
    path('view/<int:job_id>/edit-process/<int:process_id>/', views.edit_process, name="edit-process"),
    path('view/<int:job_id>/add-process/', views.add_process, name="add-process"),    
    path('view/<int:job_id>/', views.JobView.as_view(), name="view"),
    path('add', views.AddJob.as_view(), name="add"),    
    path('', views.Index, name="index"),
]