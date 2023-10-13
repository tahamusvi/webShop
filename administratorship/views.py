from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.forms import UserChangeForm, AddressForm
from accounts.models import Address
from facades.views import InformationsForTemplate
#----------------------------------------------------------------------------------------------
@login_required
def dashboard(request,address_id = None):
    profileForm = UserChangeForm(instance=request.user)
    addressForm = AddressForm()
    Info = InformationsForTemplate(request)

    if(address_id):
        address = get_object_or_404(Address,id=address_id)
        EditAddressForm = AddressForm(instance=address)
        Info["EditAddressForm"] = EditAddressForm
        Info["EditAddressId"] = address_id

    
    Info["profileForm"] = profileForm
    Info["addressForm"] = addressForm

    return render(request,'administratorship/dashboard.html',Info)
#----------------------------------------------------------------------------------------------
