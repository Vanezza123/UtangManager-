from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer_list, name='customer_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('customer/add/', views.customer_add, name='customer_add'),
    path('customer/<int:pk>/', views.customer_detail, name='customer_detail'),
    path('customer/<int:pk>/edit/', views.customer_edit, name='customer_edit'),
    path('customer/<int:pk>/delete/', views.customer_delete, name='customer_delete'),
    path('customer/<int:pk>/print/', views.customer_print, name='customer_print'),
    path('customer/<int:customer_pk>/transaction/add/', views.transaction_add, name='transaction_add'),
    path('transaction/<int:pk>/edit/', views.transaction_edit, name='transaction_edit'),
    path('transaction/<int:pk>/delete/', views.transaction_delete, name='transaction_delete'),
    path('audit-log/', views.audit_log_view, name='audit_log'),
    path('change-pin/', views.change_pin, name='change_pin'),
    path('change-password/', views.change_password, name='change_password'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('export/customers/', views.export_customers_excel, name='export_customers'),
    path('export/customer/<int:pk>/', views.export_customer_transactions_excel, name='export_customer_transactions'),
    path('export/backup/', views.export_backup_json, name='export_backup'),
]