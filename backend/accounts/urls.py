from django.urls import path
from .views import TOTPSetupView, TOTPConfirmView, TOTPVerifyView

urlpatterns = [
    path("2fa/setup/", TOTPSetupView.as_view(), name="2fa-setup"),
    path("2fa/confirm/", TOTPConfirmView.as_view(), name="2fa-confirm"),
    path("2fa/verify/", TOTPVerifyView.as_view(), name="2fa-verify"),
]