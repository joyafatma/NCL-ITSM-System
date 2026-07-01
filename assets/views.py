from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import pandas as pd

from .models import Asset, Employee, Vendor, Software, Ticket,   ExcelUpload


def login_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    error = ""

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('dashboard')

        else:

            error = "Invalid User ID or Password"

    return render(
        request,
        'login.html',
        {
            'error': error
        }
    )


def logout_view(request):

    logout(request)

    return redirect('login')


@login_required
def dashboard(request):

    context = {
        'assets_count': Asset.objects.count(),
        'employees_count': Employee.objects.count(),
        'vendors_count': Vendor.objects.count(),
        'software_count': Software.objects.count(),
        'tickets_count': Ticket.objects.count(),

        'open_tickets': Ticket.objects.filter(
            status='Open'
        ).count(),

        'resolved_tickets': Ticket.objects.filter(
            status='Resolved'
        ).count(),

        'critical_tickets': Ticket.objects.filter(
            priority='Critical'
        ).count(),
    }

    return render(
        request,
        'dashboard.html',
        context
    )


@login_required
def assets_page(request):

    assets = Asset.objects.all()

    return render(
        request,
        'assets.html',
        {
            'assets': assets
        }
    )


@login_required
def employees_page(request):

    employees = Employee.objects.all()

    return render(
        request,
        'employees.html',
        {
            'employees': employees
        }
    )


@login_required
def vendors_page(request):

    vendors = Vendor.objects.all()

    return render(
        request,
        'vendors.html',
        {
            'vendors': vendors
        }
    )


@login_required
def software_page(request):

    software = Software.objects.all()

    return render(
        request,
        'software.html',
        {
            'software': software
        }
    )


@login_required
def tickets_page(request):

    tickets = Ticket.objects.all()

    return render(
        request,
        'tickets.html',
        {
            'tickets': tickets
        }
    )
    
@login_required
def hardware_ticket(request):

    employees = Employee.objects.all()

    if request.method == "POST":

        employee_id = request.POST.get("employee")
        title = request.POST.get("title")
        asset_tag = request.POST.get("asset_tag")
        location = request.POST.get("location")
        priority = request.POST.get("priority")
        description = request.POST.get("description")

        employee = Employee.objects.get(id=employee_id)

        Ticket.objects.create(
            category="Hardware",
            title=title,
            employee=employee,
            priority=priority,
            status="Open",
            assigned_engineer="IT Support",
            description=description,
            asset_tag=asset_tag,
            location=location
        )

        return redirect('tickets')

    return render(
        request,
        'hardware_ticket.html',
        {
            'employees': employees
        }
    )

@login_required
def software_ticket(request):

    employees = Employee.objects.all()

    if request.method == "POST":

        employee_id = request.POST.get("employee")
        title = request.POST.get("title")
        impact_level = request.POST.get("impact_level")
        error_code = request.POST.get("error_code")
        priority = request.POST.get("priority")
        description = request.POST.get("description")

        employee = Employee.objects.get(id=employee_id)

        Ticket.objects.create(
            category="Software",
            title=title,
            employee=employee,
            priority=priority,
            status="Open",
            assigned_engineer="Software Team",
            description=description,
            impact_level=impact_level,
            error_code=error_code
        )

        return redirect('tickets')

    return render(
        request,
        'software_ticket.html',
        {
            'employees': employees
        }
    )


@login_required
def excel_reconciliation(request):

    duplicates = []

    if request.method == "POST":

        excel_file = request.FILES.get("excel_file")

        if excel_file:

            ExcelUpload.objects.create(
                excel_file=excel_file
            )

            df = pd.read_excel(excel_file)

            duplicate_rows = df[
                df.duplicated(
                    subset=['Material Code'],
                    keep=False
                )
            ]

            duplicates = duplicate_rows.to_dict('records')

    return render(
        request,
        'excel_reconciliation.html',
        {
            'duplicates': duplicates
        }
    )