from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *

now = timezone.now()

def home(request):
    return render(request, 'crm/home.html', {'crm' : home}) #Third argument is optional

# Create your views here.
@login_required
def customer_list(request):
    customer = Customer.objects.filter(created_date__lte=timezone.now())
    return render(request, 'crm/customer_list.html', {'customers': customer})

@login_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method=="POST":
        # update
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.updated_date = timezone.now()
            customer.save()
            customers = Customer.objects.filter(created_date__lte=timezone.now())
            return render(request, 'crm/customer_list.html', {'customers': customers})
    else:
        #edit
        form = CustomerForm(instance=customer)
    return render(request, 'crm/customer_edit.html', {'form': form})

@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    return redirect('crm:customer_list')

@login_required
def service_list(request):
    service = Service.objects.filter(created_date__lte=timezone.now())
    return render(request, 'crm/service_list.html', {'services': service})

@login_required
def service_new(request):
    if request.method == "POST":
        # update
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.created_date = timezone.now()
            service.save()
            services = Service.objects.filter(created_date__lte=timezone.now())
            return render(request, 'crm/service_list.html', {'services':services})
    else:
        form = ServiceForm()
    return render(request, 'crm/service_new.html', {'form': form})