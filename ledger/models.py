from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal


phone_validator = RegexValidator(
    regex=r'^09\d{9}$',
    message='Number must be 11 digits and start with 09 (e.g. 09123456789).'
)


class Customer(models.Model):
    name = models.CharField(max_length=255)
    number = models.CharField(
        max_length=11,
        blank=True,
        null=True,
        validators=[phone_validator]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def total_utang(self):
        result = self.transactions.filter(
            transaction_type='utang'
        ).aggregate(total=models.Sum('amount'))['total']
        return result or Decimal('0.00')

    def total_paid(self):
        result = self.transactions.filter(
            transaction_type='payment'
        ).aggregate(total=models.Sum('amount'))['total']
        return result or Decimal('0.00')

    def balance(self):
        return self.total_utang() - self.total_paid()


class Transaction(models.Model):
    TYPE_CHOICES = [
        ('utang', 'Utang'),
        ('payment', 'Payment / Partial Payment'),
    ]
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    transaction_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    note = models.TextField(blank=True)
    date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.customer.name} - {self.transaction_type} - {self.amount}"


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('create', 'Created'),
        ('edit',   'Edited'),
        ('delete', 'Deleted'),
    ]
    user      = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action    = models.CharField(max_length=10, choices=ACTION_CHOICES)
    target    = models.CharField(max_length=255)
    detail    = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user} {self.action} {self.target} @ {self.timestamp}"


class UserProfile(models.Model):
    user     = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    pin      = models.CharField(max_length=10, blank=True, null=True)
    pin_hint = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


# Signals to automatically manage UserProfile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    UserProfile.objects.get_or_create(user=instance)
    instance.profile.save()