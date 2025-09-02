from django.contrib import admin
from .models import Payment
# Register your models here.

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'payment_id', 'user', 'event', 'amount', 'created_at')
    search_fields = ('order_id', 'payment_id', 'user__username', 'event__title')
    list_filter = ('created_at', 'event')
    readonly_fields = ('uid', 'order_id', 'payment_id', 'signature', 'user', 'event', 'gatewate_response', 'amount', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': ('uid', 'order_id', 'payment_id', 'signature', 'user', 'event', 'amount')
        }),
        ('Gateway Response', {
            'fields': ('gatewate_response',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'event')

    def event_title(self, obj):
        return obj.event.title
