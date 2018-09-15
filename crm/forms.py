from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('customer_name', 'organization', 'role', 'building_room', 'account_number', 'address', 'city', 'state'
                  , 'zipcode', 'phone', 'email')