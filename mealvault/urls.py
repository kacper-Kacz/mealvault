from django.contrib import admin
from django.urls import path, include
from mealvault import error_handlers

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("accounts/", include("accounts.urls")),
    path("vault/", include("vault.urls")),
    path("payments/", include("payments.urls")),
]

handler404 = error_handlers.handle_404
handler500 = error_handlers.handle_500
handler403 = error_handlers.handle_403
