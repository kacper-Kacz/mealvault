from django.contrib import admin
from .models import PaymentEvent

@admin.register(PaymentEvent)
class PaymentEventAdmin(admin.ModelAdmin):
    list_display = ("event_type", "stripe_event_id", "user", "created_at")
    search_fields = ("stripe_event_id", "event_type", "user__username")
    list_filter = ("event_type",)
