from django.urls import path
from .views import visit_counter, reset_visit_counter

from django.contrib.auth import views as auth_views

urlpatterns = [
    path("visits/", visit_counter, name="visit_counter"),
    path("visits/reset/", reset_visit_counter, name="reset_visit_counter"),
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            template_name="accounts/registration/password_change.html"
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="accounts/registration/password_change_done.html"
        ),
        name="password_change_done",
    ),
]
