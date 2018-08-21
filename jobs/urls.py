from django.urls import path
from . import views

app_name = "jobs"

urlpatterns = [
    path('view/<int:job_id>', views.JobView.as_view(), name="view"),
    path('add', views.AddJob.as_view(), name="add"),
    path('', views.Index, name="index"),
]