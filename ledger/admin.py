from django.contrib import admin
from .models import Customer, Transaction, AuditLog


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'number', 'balance', 'created_at']
    search_fields = ['name', 'number']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['customer', 'transaction_type', 'amount', 'date', 'note']
    list_filter = ['transaction_type']
    search_fields = ['customer__name', 'note']
    date_hierarchy = 'date'


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'target', 'timestamp']
    list_filter = ['action']
    search_fields = ['target', 'detail']