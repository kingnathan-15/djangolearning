from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Sites, Credentials
from .encrypt import AESEncryption
from .forms import SitesForm, CredentialsAddForm

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
    context = {}
    return render(request, "register.html", context)


def login_page(request):
    context = {}
    return render(request, "login.html", context)


@login_required
def add_creds(request):
    all_sites = Sites.objects.all()
    if request.method == "POST":
        form = SitesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("site_list")
    else:
        form = SitesForm()
    return render(request, "index.html", {"results": all_sites, "form": form})


@login_required
def check_accounts(request, site_id):
    all_accounts = Credentials.objects.filter(Site=site_id)
    encrypt_instance= AESEncryption()

    for accounts in all_accounts:
        accounts.password = encrypt_instance.decrypt_passwords("123", accounts.password)
    site = Sites.objects.get(id=site_id)
    if request.method == "POST":
        form = CredentialsAddForm(request.POST)
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
