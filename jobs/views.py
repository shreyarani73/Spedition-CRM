from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .models import Job, Process
from .forms import NewJobForm, UpdateJobForm, ProcessForm, UpdateProcessForm
from invoices.models import Invoice, Payments
from expenses.models import Expense
from django.db.models import Sum

def Index(request):
    all_jobs = Job.objects.all()

    return render(request, "jobs/index.html", {
        "jobs": all_jobs,
    })


class AddJob(View):
    def get(self, request ):
        form = NewJobForm()

        return render(request, "jobs/add.html", {
            "form":form,
        })

    def post(self, request):
        new_job = NewJobForm(request.POST)
        job = new_job.save() #error if not valid data

        messages.add_message(request, messages.SUCCESS, "Your new job has been created")

        return redirect("jobs:view", job_id=job.id)

class JobView(View):
    def get(self, request, job_id):
        job = Job.objects.get(pk=job_id)
        form = UpdateJobForm(instance=job)
        processForm = ProcessForm()

        expenses = Expense.objects.filter(job=job)
        expenses_total = expenses.aggregate(Sum("amount"))["amount__sum"]

        invoices = Invoice.objects.filter(job=job)
        invoices_total = invoices.aggregate(Sum("total"))["total__sum"]        

        try:
            netpl = invoices_total - expenses_total
        except:
            netpl = "There are no invoices or expenses for this bill"

        processes = Process.objects.filter(job=job).order_by("-date_added")
        process_forms = []
        for each in processes:
            form = ProcessForm(instance=each)
            form.id = each.id
            process_forms.append(form)
            print (form.id)

        return render(request, "jobs/job.html", {
            "job":job, "form": form, "netpl": netpl,
            "expenses": expenses, "expenses_total": expenses_total,
            "invoices": invoices, "invoices_total": invoices_total,
            "processes": process_forms, "processForm": processForm
        })

    def post(self, request, job_id):
        job = Job.objects.get(pk=job_id)
        form = UpdateJobForm(request.POST, instance=job)
        form.save()        

        messages.add_message(request, messages.SUCCESS, "Job has been succesfully updated")

        return redirect("jobs:view", job_id=job_id)


def add_process(request, job_id):
    form = ProcessForm(request.POST)
    job = Job.objects.get(pk=job_id)
    process = form.save(commit=False)
    process.job = job
    process.save()

    messages.add_message(request, messages.SUCCESS, "New process has been succesfully created")

    return redirect("jobs:view", job_id=job_id)
    

def edit_process(request, job_id, process_id):
    process = Process.objects.get(id=process_id)
    form = ProcessForm(request.POST, instance=process)
    eProcess = form.save()

    messages.add_message(request, messages.SUCCESS, "Process has been succesfully edited")

    return redirect("jobs:view", job_id=job_id)

def delete_process(request, job_id, process_id):
    process = Process.objects.get(id=process_id)
    job = Job.objects.get(id=job_id)
    process.delete()

    messages.add_message(request, messages.SUCCESS, "Process has been succesfully deleted")

    return redirect("jobs:view",job_id=job_id)

