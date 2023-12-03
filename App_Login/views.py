from django.shortcuts import render,HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy

# authentication
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

# forms and models
from App_Login.models import Profile
from App_Login.forms import ProfileForm, SignUpForm

# Messages
from django.contrib import messages

# Create your views here.


def sign_up(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Created Successfully')
            return HttpResponseRedirect(reverse('login'))
    return render(request, 'App_Login/sign_up.html', context={'form':form})


def login_user(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponse('Logged In')          
    return render(request, 'App_Login/login.html', context={'form':form})


@login_required
def logout_user(request):
    logout(request)
    messages.warning(request, 'You are logged out')
    return HttpResponse('Logged Out')


@login_required
def user_profile(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(instance=profile)
    if form.is_valid():
        form.save()
        messages.success(request, 'Change Saved')
        form = ProfileForm(instance=profile)
    return render(request, "App_Login/change_profile.html", context={'form':form})



