from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import CreateView
from django.shortcuts import render
from .models import Customer as CustomerModel
from .models import Documents
from .forms import CustomerForm, CustomerUpdateForm
from django.contrib import messages


class Customers(View):
    def get(self, request):
        customers = CustomerModel.objects.all()

        return render(request, "customers/index.html", {
            "customers":customers,
        })


class AddCustomer(View):
    def get(self, request):
        form = CustomerForm()

        return render(request, "customers/add.html", {
            "form":form,
        })

    def post(self, request):
        form = CustomerForm(request.POST)
        new_customer = form.save()        

        return redirect("customers:view", customer_id=new_customer.pk)


class CustomerView(View):
    def get(self, request, customer_id):        
        customer = CustomerModel.objects.get(pk=customer_id)
        documents = Documents.objects.filter(customer=customer)

        form = CustomerUpdateForm(instance=customer)

        return render(request, "customers/customer.html", {
            "form":form, "documents":documents, "customer": customer,
        })

    def post(self, request, customer_id):
        customer = CustomerModel.objects.get(pk=customer_id)
        form = CustomerUpdateForm(request.POST, instance=customer)
        updated = form.save()

        messages.add_message(request, messages.SUCCESS, "Company has been updated")

        return redirect("customers:view", customer_id=customer_id)



def CustomerFileUpload(request, customer_id):
    customer = CustomerModel.objects.get(pk=customer_id)
    document_type = request.POST.get("document_type")
    document_file = request.FILES["document_file"]

    new_document = Documents(customer=customer, document_type=document_type, document_file=document_file)
    try:
        new_document.save()
    except:
        messages.add_message(request, messages.FAILURE, "Please check the document you uploaded and try again")
    else:
        messages.add_message(request, messages.SUCCESS, "Document uploaded succesfully")

    return redirect("customers:view", customer_id=customer_id)   
