from django.urls import path
from .views import pricing, create_checkout_session, success, cancel
from .webhook import stripe_webhook

app_name = "payments"

urlpatterns = [
    path("pricing/", pricing, name="pricing"),
    path("checkout/", create_checkout_session, name="checkout"),
    path("success/", success, name="success"),
    path("cancel/", cancel, name="cancel"),
    path("webhook/stripe/", stripe_webhook, name="stripe_webhook"),
]
