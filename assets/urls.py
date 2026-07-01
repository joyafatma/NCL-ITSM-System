from django.urls import path
from .views import (
    login_view,
    logout_view,
    dashboard,
    assets_page,
    employees_page,
    vendors_page,
    software_page,
    tickets_page,
    hardware_ticket,
    software_ticket,
    excel_reconciliation,
)

urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('dashboard/', dashboard, name='dashboard'),

    path('assets/', assets_page, name='assets'),
    path('employees/', employees_page, name='employees'),
    path('vendors/', vendors_page, name='vendors'),
    path('software/', software_page, name='software'),
    path('tickets/', tickets_page, name='tickets'),

    path('hardware-ticket/', hardware_ticket, name='hardware_ticket'),
    path('software-ticket/', software_ticket, name='software_ticket'),
    path(
    'excel-reconciliation/',
    excel_reconciliation,
    name='excel_reconciliation'
    ),
]