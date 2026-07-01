from django.db import models


class Asset(models.Model):
    asset_name = models.CharField(max_length=100)
    asset_type = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    status = models.CharField(max_length=50)

    assigned_to = models.ForeignKey(
        'Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.asset_name


class Employee(models.Model):
    employee_id = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Vendor(models.Model):
    vendor_name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.vendor_name


class Software(models.Model):
    software_name = models.CharField(max_length=100)
    version = models.CharField(max_length=50)
    license_key = models.CharField(max_length=100)
    expiry_date = models.DateField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.software_name


class Ticket(models.Model):

    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Assigned', 'Assigned'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ]

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]

    CATEGORY_CHOICES = [
        ('Hardware', 'Hardware'),
        ('Software', 'Software'),
    ]

    ticket_id = models.CharField(
        max_length=30,
        unique=True,
        blank=True
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )

    title = models.CharField(max_length=200)

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Open'
    )

    assigned_engineer = models.CharField(
        max_length=100,
        blank=True
    )

    description = models.TextField()

    # New fields according to PDF

    asset_tag = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    location = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    impact_level = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    error_code = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    # Hardware Ticket Fields

    HARDWARE_TYPE_CHOICES = [
        ('Desktop', 'Desktop'),
        ('Laptop', 'Laptop'),
        ('Printer/Scanner', 'Printer/Scanner'),
        ('IP Phone', 'IP Phone'),
        ('Network/Wi-Fi', 'Network/Wi-Fi'),
        ('Peripherals', 'Peripherals'),
    ]

    hardware_type = models.CharField(
        max_length=50,
        choices=HARDWARE_TYPE_CHOICES,
        blank=True,
        null=True
    )


    # Software Ticket Fields

    SOFTWARE_CATEGORY_CHOICES = [
        ('Windows OS', 'Windows OS'),
        ('Antivirus', 'Antivirus'),
        ('PDF Reader', 'PDF Reader'),
        ('Browser Issues', 'Browser Issues'),
        ('Local Driver Software', 'Local Driver Software'),
    ]

    software_category = models.CharField(
        max_length=100,
        choices=SOFTWARE_CATEGORY_CHOICES,
        blank=True,
        null=True
    )


    # File Uploads

    attachment = models.FileField(
        upload_to='hardware_attachments/',
        blank=True,
        null=True
    )

    screenshot = models.FileField(
    upload_to='software_screenshots/',
    blank=True,
    null=True
)
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):

        if not self.ticket_id:

            last_ticket = Ticket.objects.order_by('id').last()

            if last_ticket and last_ticket.ticket_id:
                try:
                    last_id = int(last_ticket.ticket_id.split('-')[-1])
                    new_id = last_id + 1
                except:
                    new_id = 1
            else:
                new_id = 1

            self.ticket_id = f"INC-2026-{new_id:04d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.ticket_id
    
class ExcelUpload(models.Model):

    excel_file = models.FileField(
        upload_to='excel_files/'
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.excel_file.name