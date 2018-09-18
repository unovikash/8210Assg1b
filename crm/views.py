from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
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
def customer_new(request):
    if request.method=="POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.created_date = timezone.now()
            customer.save()
            customers = Customer.objects.filter(created_date__lte=timezone.now())
            return render(request, 'crm/customer_list.html', {'customers': customers})
    else:
        form = CustomerForm()
    return render(request, 'crm/customer_edit.html', {'form': form})

@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    return redirect('crm:customer_list')

@login_required
def summary(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    products = Product.objects.filter(customer_name=pk)
    sum_product_charge = Product.objects.filter(customer_name=pk).aggregate(Sum('charge'))
    services = Service.objects.filter(customer_name=pk)
    sum_service_charge = Service.objects.filter(customer_name=pk).aggregate(Sum('service_charge'))
    return render(request, 'crm/summary.html', {'products': products, 'sum_product_charge': sum_product_charge
                                                , 'services': services, 'sum_service_charge': sum_service_charge})

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

@login_required
def service_edit(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == "POST":
        #update
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            service = form.save(commit=False)
            service.updated_date = timezone.now()
            service.save()
            services = Service.objects.filter(created_date__lte=timezone.now())
            return render(request, 'crm/service_list.html', {'services':services})
    else:
        form=ServiceForm(instance=service)
    return render(request, 'crm/service_edit.html', {'form':form})

@login_required
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    service.delete()
    return redirect('crm:customer_list')

@login_required
def product_list(request):
    products = Product.objects.filter(created_date__lte=timezone.now())
    return render(request, 'crm/product_list.html', {'products': products})

@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method=="POST":
        # update
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.updated_date = timezone.now()
            product.save()
            products = Product.objects.filter(created_date__lte=timezone.now())
            return render(request, 'crm/product_list.html', {'products': products})
    else:
        #edit
        form = ProductForm(instance=product)
    return render(request, 'crm/product_edit.html', {'form': form})

@login_required
def product_new(request):
    if request.method=="POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_date = timezone.now()
            product.save()
            products = Product.objects.filter(created_date__lte=timezone.now())
            return render(request, 'crm/product_list.html', {'products': products})
    else:
        form = ProductForm()
    return render(request, 'crm/product_edit.html', {'form': form})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('crm:product_list')

def signup(request):
    if request.method=="POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return render(request, 'crm/home.html')
    else:
        form = UserForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def change_password(request):
    if request.method=='POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated')
            return render(request, 'crm/home.html')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {'form': form})