from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    serial_no = models.CharField(max_length=100, unique=True)
    available = models.BooleanField(default=True)
   

    def __str__(self):
        return f"{self.name} ({self.serial_no})"


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    issue_date = models.DateField(default=timezone.now)
    due_date = models.DateField(blank=True, null=True)
    return_date = models.DateField(blank=True, null=True)

    returned = models.BooleanField(default=False)
    fine = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        # Automatically set due date = issue_date + 7 days
        if not self.due_date:
            self.due_date = self.issue_date + timedelta(days=7)
        super().save(*args, **kwargs)

    def calculate_fine(self):
        if self.return_date and self.return_date > self.due_date:
            late_days = (self.return_date - self.due_date).days
            return late_days * 10
        return 0
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateField(default=timezone.now)
    return_date = models.DateField(blank=True, null=True)
    
    returned = models.BooleanField(default=False)
    fine = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        if not self.return_date:
            self.return_date = timezone.now().date() + timedelta(days=7)
        super().save(*args, **kwargs)

    def fine(self):
        if not self.returned and timezone.now().date() > self.return_date:
            late_days = (timezone.now().date() - self.return_date).days
            return late_days * 10
        return 0