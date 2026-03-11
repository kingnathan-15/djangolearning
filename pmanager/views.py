from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from django.contrib import messages

from .models import Sites, Credentials
from .encrypt import AESEncryption
from .forms import SitesForm, CredentialsAddForm, CreateUserForm, LoginForm

# def master_password(request):
#     x = AESEncryption()
#     if (x.status == False):
#         x.create_master_password()
#     else:
#         if (x.master_password):
#             x.verify_master_password()
#             return redirect('master_password')
#         else:
#             return redirect('site_list')
#     return redirect()


def register_page(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CreateUserForm()
    return render(request, "register.html", {"form":form, "title": "Register New User", "button_text":"Register"})


def login_page(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('site_list')
            else:
                messages.info(request, 'Username or Password is incorrect')

    context = {
        "form": form,
        "title": "Login",
        "button_text": "Login"
    }
    return render(request, "login.html", context)


@login_required
def add_creds(request):
    all_sites = Sites.objects.all()
    print(request.user.id)
    if request.method == "POST":
        form = SitesForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.user = request.user.username
            print(request.user.username)
            form.save()
            return redirect("site_list")
    else:
        form = SitesForm()
    return render(request, "index.html", {"results": all_sites, "form": form})


@login_required
def check_accounts(request, site_id):
    all_accounts = Credentials.objects.filter(Site=site_id)
    encrypt_instance= AESEncryption()
    authstring = request.user.username + request.user.password
    
    for accounts in all_accounts:
        accounts.password = encrypt_instance.decrypt_passwords(str(authstring), accounts.password)
    site = Sites.objects.get(id=site_id)
    if request.method == "POST":
        form = CredentialsAddForm(request.POST, request=request)
        if form.is_valid():
            form.Site = site
            form.save()
            return redirect("check_users", site_id=site_id)
    else:
        form = CredentialsAddForm(initial={"Site": site})
    return render(
        request,
        "accounts.html",
        {"results": all_accounts, "site_id": site, "form": form},
    )
