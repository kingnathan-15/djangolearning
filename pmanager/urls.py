from django.urls import path, include
from . import views

urlpatterns = [
    path("accounts/login/", views.login_page, name = "login"),
    path("accounts/register/", views.register_page, name = "register"),
    path("", views.add_creds, name="site_list"),
    path("user_page/<int:site_id>/", views.check_accounts, name="check_users"),
]
