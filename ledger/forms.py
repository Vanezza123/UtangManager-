from django import forms
import re
from .models import Customer, Transaction
from django.utils import timezone

class CustomerForm(forms.ModelForm):
    name = forms.CharField(
        label='Customer Name',
        strip=True,
        error_messages={'required': 'Customer name is required.'},
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Customer name (required)',
            'autofocus': True,
        }),
    )
    number = forms.CharField(
        label='Phone Number',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '09XXXXXXXXX',
            'maxlength': '11',
            'pattern': '09[0-9]{9}',
            'inputmode': 'numeric',
        }),
        help_text='Optional. 11-digit number starting with 09.',
    )

    class Meta:
        model  = Customer
        fields = ['name', 'number']

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()

        if not name:
            raise forms.ValidationError('Customer name cannot be blank.')

        # Enforce only words/letters and spaces. No numbers, dots, or special characters.
        if not re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$", name):
            raise forms.ValidationError(
                'Customer name must contain letters and spaces only. No numbers, dots, or symbols allowed.'
            )

        # Format name to Title Case (capitalize first letter of each word)
        name = " ".join([word.capitalize() for word in name.split()])

        qs = Customer.objects.filter(name__iexact=name)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(
                f'The name "{name}" already exists. Please add a middle name or last name '
                'to make the customer name unique.'
            )

        return name

    def clean_number(self):
        number = self.cleaned_data.get('number', '').strip()
        if not number:
            return ''
        if not number.isdigit():
            raise forms.ValidationError('Number must contain digits only, no spaces or dashes.')
        if len(number) != 11:
            raise forms.ValidationError('Number must be exactly 11 digits.')
        if not number.startswith('09'):
            raise forms.ValidationError('Number must start with 09.')
        return number


class TransactionForm(forms.ModelForm):
    class Meta:
        model   = Transaction
        fields  = ['transaction_type', 'amount', 'note', 'date']
        widgets = {
            'transaction_type': forms.Select(attrs={
                'class': 'form-select form-select-lg',
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'step': '0.01',
                'min': '0.01',
                'placeholder': '0.00',
                'inputmode': 'decimal',
            }),
            'note': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Optional note...',
            }),
            'date': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local',
                },
                format='%Y-%m-%dT%H:%M',
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['date'].initial = timezone.localtime(
                timezone.now()
            ).strftime('%Y-%m-%dT%H:%M')

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is None:
            raise forms.ValidationError("Please enter a valid amount.")
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        return amount


class ChangePinForm(forms.Form):
    current_pin = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter current PIN'}),
        label='Current PIN',
    )
    new_pin = forms.CharField(
        max_length=10,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter new PIN (4-10 digits)'}),
        label='New PIN',
    )
    confirm_pin = forms.CharField(
        max_length=10,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm new PIN'}),
        label='Confirm New PIN',
    )
    pin_hint = forms.CharField(
        required=False,
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. My birthday year'}),
        label='PIN Hint (optional)',
        help_text='A hint shown on the forgot password page to help you remember.',
    )

    def clean_new_pin(self):
        pin = self.cleaned_data.get('new_pin', '')
        if not pin.isdigit():
            raise forms.ValidationError('PIN must be numbers only.')
        if len(pin) < 4:
            raise forms.ValidationError('PIN must be at least 4 digits.')
        return pin

    def clean(self):
        cleaned = super().clean()
        new_pin     = cleaned.get('new_pin')
        confirm_pin = cleaned.get('confirm_pin')
        if new_pin and confirm_pin and new_pin != confirm_pin:
            raise forms.ValidationError('PINs do not match.')
        return cleaned


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Current password'}),
        label='Current Password',
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New password'}),
        label='New Password',
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm new password'}),
        label='Confirm New Password',
    )

    def clean(self):
        cleaned = super().clean()
        new_pw      = cleaned.get('new_password')
        confirm_pw  = cleaned.get('confirm_password')
        if new_pw and confirm_pw and new_pw != confirm_pw:
            raise forms.ValidationError('New passwords do not match.')
        return cleaned


class ForgotPasswordPinForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your username'}),
        label='Username',
    )
    pin = forms.CharField(
        max_length=10,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Your PIN'}),
        label='PIN',
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New password'}),
        label='New Password',
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm new password'}),
        label='Confirm New Password',
    )

    def clean(self):
        cleaned = super().clean()
        new_pw     = cleaned.get('new_password')
        confirm_pw = cleaned.get('confirm_password')
        if new_pw and confirm_pw and new_pw != confirm_pw:
            raise forms.ValidationError('New passwords do not match.')
        return cleaned