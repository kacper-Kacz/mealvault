import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

stripe.api_key = settings.STRIPE_SECRET_KEY

def pricing(request):
    return render(request, "payments/pricing.html", {
        "stripe_pk": settings.STRIPE_PUBLISHABLE_KEY,
        "price_gbp": "4.99",
    })

@login_required
def create_checkout_session(request):
    if not settings.STRIPE_SECRET_KEY:
        messages.error(request, "Stripe is not configured. Add keys to your environment.")
        return redirect("payments:pricing")

    success_url = f"{settings.SITE_URL}{reverse('payments:success')}"
    cancel_url = f"{settings.SITE_URL}{reverse('payments:cancel')}"

    # One-time purchase unlocks premium access
    session = stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "gbp",
                "product_data": {"name": "MealVault Premium Pass"},
                "unit_amount": 499,
            },
            "quantity": 1,
        }],
        metadata={"user_id": str(request.user.id)},
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return redirect(session.url, code=303)

@login_required
def success(request):
    messages.success(request, "Payment successful! Your Premium access will be activated shortly.")
    return redirect("accounts:profile")

@login_required
def cancel(request):
    messages.info(request, "Payment cancelled. You can try again any time.")
    return redirect("payments:pricing")
