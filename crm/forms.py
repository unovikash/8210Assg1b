from django import forms
from .models import Customer, Service

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('customer_name', 'organization', 'role', 'building_room', 'account_number', 'address', 'city'
                  , 'state', 'zipcode', 'phone', 'email')

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ('customer_name', 'service_category', 'description', 'location', 'setup_time', 'cleanup_time'
                  , 'service_charge')