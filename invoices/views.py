from django.shortcuts import render, redirect
from django.views import View
from .models import Invoice, InvoiceItem, Payments
from .forms import NewInvoice, InvoiceItemForm, NewInvoiceItemForm, InvoicePaymentForm, NewInvoicePaymentForm
from django.contrib import messages

def Index(request):
    invoices = Invoice.objects.all()

    return render(request, "invoices/index.html", {
        "invoices":invoices,
    })


class AddInvoice(View):
    def get(self, request):
        form = NewInvoice()

        return render(request, "invoices/add.html", {
            "form": form,
        })

    def post(self, request):
        form = NewInvoice(request.POST)
        invoice = form.save(commit=False)
        invoice.total = 0
        invoice.save()
        invoice.invoice_id="SPEDITION/INVOICE/%s" % (invoice.pk)
        invoice.save()


        return redirect("invoices:view", invoice_id=invoice.pk)


class InvoiceView(View):
    def get(self, request, invoice_id):
        invoice = Invoice.objects.get(pk=invoice_id)
        invoice_items = InvoiceItem.objects.filter(invoice=invoice)
        invoice_items_forms = []
        new_invoice_item_form = NewInvoiceItemForm()        

        payments = Payments.objects.filter(invoice=invoice)
        payment_forms = []
        new_payment_form = NewInvoicePaymentForm()
        for each in payments:
            form = InvoicePaymentForm(instance=each)
            payment_forms.append(form)
        
        for each in invoice_items:
            form = InvoiceItemForm(instance=each)
            invoice_items_forms.append(form)

        return render(request, "invoices/view.html", {
            "invoice": invoice, "invoice_items": invoice_items_forms,
            "new_invoice_item_form": new_invoice_item_form, "payment_forms": payment_forms,
            "new_payment_form": new_payment_form
        })

    def post(self, request, invoice_id):
        pass


def NewInvoiceItem(request, invoice_id):
    invoice = Invoice.objects.get(pk=invoice_id)
    form = NewInvoiceItemForm(request.POST)
    invoice_item = form.save(commit=False)
    invoice_item.invoice = invoice
    sub_total = invoice_item.quantity * invoice_item.rate * invoice_item.exchange_rate
    tax = sub_total * invoice_item.tax_rate/100
    sub_total = sub_total + tax
    

    invoice_item.total = sub_total

    invoice.total = invoice.total + sub_total
    
    client = invoice.job.client
    client.credit_amount = client.credit_amount - sub_total
    if client.credit_amount < 0:
        messages.add_message(request, messages.SUCCESS, "Credit amount not enough for client")
        return redirect("invoices:view", invoice_id=invoice_id)
    else:
        client.save()

        invoice.save()
        invoice_item.save()

        messages.add_message(request, messages.SUCCESS, "Invoice item added")

        return redirect("invoices:view", invoice_id=invoice_id)


def AddPaymentToInvoice(request, invoice_id):
    invoice = Invoice.objects.get(pk=invoice_id)
    form = NewInvoicePaymentForm(request.POST)
    payment = form.save(commit=False)
    payment.invoice = invoice
    
    invoice.total = invoice.total - payment.amount
    client = invoice.job.client
    client.credit_amount = client.credit_amount + payment.amount
    
    client.save()
    payment.save()
    invoice.save()

    return redirect("invoices:view", invoice_id=invoice_id)