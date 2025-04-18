from django.shortcuts import render, redirect

from . forms import CreateUserForm,LoginForm

from django.contrib.auth.decorators import login_required

#Authentication models and functions
from django.contrib.auth.models import auth

from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponseForbidden


# Create your views here.
def homepage(request):

    return render(request, 'sch_spark/index.html')



def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("my-login")

    context = {'registerform':form}
    return render(request, 'sch_spark/register.html', context=context)



def my_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
            return redirect("dashboard")
    context =  {'loginform':form}           
            
    return render(request, 'sch_spark/my-login.html', context=context)

def user_logout(request):
    auth.logout(request)
    return redirect("")


@login_required(login_url='my-login')
def dashboard(request):   

    return render(request, 'sch_spark/dashboard.html')

 # Show the teacher dashboard
def teacher_dashboard(request):
    if request.user.profile.role != 'teacher':
        return HttpResponseForbidden("You don't have permission.")