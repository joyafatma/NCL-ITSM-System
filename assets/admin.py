from django.contrib import admin
from .models import Asset, Employee, Vendor, Software, Ticket


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):

    list_display = (
        'asset_name',
        'asset_type',
        'serial_number',
        'status',
        'assigned_to'
    )

    search_fields = (
        'asset_name',
        'serial_number',
        'assigned_to__name'
    )

    list_filter = (
        'asset_type',
        'status'
    )


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    list_display = (
        'employee_id',
        'name',
        'department',
        'email'
    )

    search_fields = (
        'employee_id',
        'name'
    )

    list_filter = (
        'department',
    )


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):

    list_display = (
        'vendor_name',
        'contact_person',
        'phone',
        'email'
    )

    search_fields = (
        'vendor_name',
        'contact_person'
    )


@admin.register(Software)
class SoftwareAdmin(admin.ModelAdmin):

    list_display = (
        'software_name',
        'version',
        'expiry_date',
        'status'
    )

    search_fields = (
        'software_name',
        'version'
    )

    list_filter = (
        'status',
    )


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):

    list_display = (
        'ticket_id',
        'category',
        'title',
        'employee',
        'priority',
        'status',
        'assigned_engineer',
        'created_at'
    )

    search_fields = (
        'ticket_id',
        'title',
        'employee__name',
        'assigned_engineer'
    )

    list_filter = (
        'category',
        'priority',
        'status'
    )

    readonly_fields = (
        'ticket_id',
        'created_at',
        'updated_at'
    )