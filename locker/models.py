from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class Document(models.Model):
    CATEGORY_CHOICES = [
        ('ID', 'ID Proof'),
        ('EDU', 'Education'),
        ('CERT', 'Certificates'),
        ('BILL', 'Bills & Utilities'),
        ('INSURANCE', 'Insurance'),
        ('OTHER', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)

    file = models.FileField(
        upload_to='documents/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'pdf'])]
    )

    # 🔥 NEW FIELD (THIS IS THE KEY)
    thumbnail = models.ImageField(
        upload_to='thumbnails/',
        null=True,
        blank=True
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
