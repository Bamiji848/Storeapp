from django import forms
from django.core import validators
from django.conf import settings
from django.forms.fields import DateTimeField
from django.forms.widgets import DateTimeBaseInput, DateTimeInput
from store.models import *
from django.contrib.auth.forms import(
    PasswordResetForm, SetPasswordForm, PasswordChangeForm,
    UserChangeForm, UserCreationForm)
from datetime import date


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Old Password'}))
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'New Password'}))
    new_password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
    botcatcher = forms.CharField(required=False, widget=forms.HiddenInput, validators=[
                                 validators.MaxLengthValidator(0)])


class PackagedForm(forms.ModelForm):
    packaged = forms.BooleanField(
        required=True, label='Tick only if item has been accurately packaged')

    class Meta():
        model = Inventory
        fields = ['packaged']


class DisbursedForm(forms.ModelForm):
    disburse = forms.BooleanField(
        required=True, label='Tick only if item has been duly collected by parent/student/guardian')

    class Meta():
        model = Inventory
        fields = ['disburse']


class DateInput(forms.DateInput):
    input_type = 'date'


class DateRangeForm(forms.Form):
    start_date = forms.DateTimeField(
        label='From:', widget=DateInput(attrs={'class': 'form-control'}))
    end_date = forms.DateTimeField(
        label='To:', widget=DateInput(attrs={'class': 'form-control'}))
