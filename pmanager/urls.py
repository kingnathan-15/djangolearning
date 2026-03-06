from django.urls import path
from . import views

urlpatterns = [
    # path("", views.master_password, name="master"),
    path("", views.add_creds, name="site_list"),
    path("login", views.loginPage, name = "login"),
    path("register", views.registerPage, name = "register"),
    path("user_page/<int:site_id>/", views.check_accounts, name="check_users"),
]
