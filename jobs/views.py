from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .models import Job
from .forms import NewJobForm, UpdateJobForm

def Index(request):
    all_jobs = Job.objects.all()

    return render(request, "jobs/index.html", {
        "jobs": all_jobs,
    })


class AddJob(View):
    def get(self, request):
        form = NewJobForm()

        return render(request, "jobs/add.html", {
            "form":form,
        })

    def post(self, request):
        new_job = NewJobForm(request.POST)
        new_job.save()

        messages.add_message(request, messages.SUCCESS, "Your new job has been created")

        return redirect("jobs:view", job_id=new_job.id)

class JobView(View):
    def get(self, request, job_id):
        job = Job.objects.get(pk=job_id)
        form = UpdateJobForm(instance=job)

        return render(request, "jobs/job.html", {
            "job":job, "form": form,
        })

    def post(self, request, job_id):
        job = Job.objects.get(pk=job_id)
        form = UpdateJobForm(request.POST, instance=job)
        form.save()

        print (form.errors)

        messages.add_message(request, messages.SUCCESS, "Job has been succesfully updated")

        return redirect("jobs:view", job_id=job_id)