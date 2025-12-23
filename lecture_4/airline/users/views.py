from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import redirect
# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    
    return render(request, "users/user.html", {
        "user": User.objects.get(pk=request.user.id)
    })


def login_request(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print("User authenticated")
            login(request, user)
            return HttpResponseRedirect(reverse("users:index")) 

        return render(request, "users/login.html", {
            "message": "Invalid credentials"
        })
    
    return render(request, "users/login.html")

def logout_request(request):
    logout(request)
    return render(request, "users/login.html",{
        "message": "You have been logged out"
    })
