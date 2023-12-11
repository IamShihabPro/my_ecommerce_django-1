from django.forms import ModelForm
from App_Payment.models import BillingAddress




class BillingForm(ModelForm):
    class Meta:
        model = BillingAddress
        fields = ['address', 'zipcode', 'city', 'country']
        