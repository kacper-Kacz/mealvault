import json
import stripe
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

from accounts.models import Profile
from .models import PaymentEvent

User = get_user_model()

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")

    if not settings.STRIPE_WEBHOOK_SECRET:
        return HttpResponseBadRequest("Webhook secret not set.")

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=settings.STRIPE_WEBHOOK_SECRET,
        )
    except ValueError:
        return HttpResponseBadRequest("Invalid payload.")
    except stripe.error.SignatureVerificationError:
        return HttpResponseBadRequest("Invalid signature.")

    # Idempotency: never process same event twice
    if PaymentEvent.objects.filter(stripe_event_id=event["id"]).exists():
        return HttpResponse(status=200)

    user = None
    data = event.get("data", {}).get("object", {})
    user_id = None

    # Checkout session carries metadata
    if event["type"] == "checkout.session.completed":
        meta = data.get("metadata", {})
        user_id = meta.get("user_id")

    if user_id:
        try:
            user = User.objects.get(id=int(user_id))
        except (User.DoesNotExist, ValueError, TypeError):
            user = None

    PaymentEvent.objects.create(
        user=user,
        stripe_event_id=event["id"],
        event_type=event["type"],
        raw=json.loads(payload.decode("utf-8")) if payload else {},
    )

    if event["type"] == "checkout.session.completed" and user:
        profile, _ = Profile.objects.get_or_create(user=user)
        profile.is_premium = True
        if not profile.premium_since:
            profile.premium_since = timezone.now()
        profile.save()

    return HttpResponse(status=200)
