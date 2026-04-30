from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {
                "error": "Username already exists"
            })

        User.objects.create_user(username=username, password=password)
        return redirect("login")

    return render(request, "register.html")


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("chat")
        else:
            return render(request, "login.html", {
                "error": "Invalid username or password"
            })

    return render(request, "login.html")


from django.contrib.auth import logout
from django.shortcuts import redirect

def user_logout(request):
    response = redirect("login")

    # logout user (clears session)
    logout(request)

    # delete all cookies manually
    for key in request.COOKIES.keys():
        response.delete_cookie(key)

    return response



from django.views.decorators.cache import cache_control

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def chat(request):
    if not request.user.is_authenticated:
        return redirect("login")
    
    return render(request, "chat.html")

from django.contrib.auth.decorators import login_required

@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def chat(request):
    return render(request, "chat.html")