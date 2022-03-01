from django import forms
from django.forms import fields, widgets

from storeapp.views import packaged
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core import validators

from store.models import Inventory


class CategoryForm(forms.ModelForm):
    class Meta():
        model = Category
        fields = '__all__'


class ShopProductForm(forms.ModelForm):
    class Meta():
        model = ShopProduct
        fields = ['product_name1', 'product_price1']


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 26)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput)


class DateInput(forms.DateInput):
    input_type = 'upload_date'


class InventoryForm(forms.ModelForm):
    active = forms.BooleanField(required=True, label='Tick to Proceed')
    paymentmode = forms.ModelChoiceField(label="Mode of Payment", queryset=PaymentMode.objects.all(
    ), widget=forms.Select(attrs={'class': 'form-control'}))
    parenttel = forms.CharField(label="Parent's Whatsapp Phone Number",
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "e.g 2348030112233"}))

    class Meta():
        model = Inventory
        fields = ['studentrecord', 'studentclass',
                  'sex', 'size', 'paymentmode', 'account', 'parenttel', 'active']


def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['studentclass'].queryset = StudentClass.objects.none()
    # self.fields['class_arm'].queryset = ClassArm.objects.none()
    self.fields['sex'].queryset = Gender.objects.none()
    # self.fields['program_type'].queryset = ProgramType.objects.none()

    if 'studentrecord' in self.data:
        try:
            studentrecord_id = int(self.data.get('studentrecord'))
            self.fields['studentclass'].queryset = StudentClass.objects.filter(
                studentrecord_id=studentrecord_id).order_by('studentclass')
        except (ValueError, TypeError):
            pass  # invalid input from the client; ignore and fallback to empty City queryset
    elif self.instance.pk:
        self.fields['studentclass'].queryset = self.instance.studentrecord.studentclass_set.order_by(
            'studentclass')

    # if 'studentrecord' in self.data:
    #     try:
    #         studentrecord_id = int(self.data.get('studentrecord'))
    #         self.fields['class_arm'].queryset = ClassArm.objects.filter(
    #             studentrecord_id=studentrecord_id).order_by('class_arm')
    #     except (ValueError, TypeError):
    #         pass  # invalid input from the client; ignore and fallback to empty City queryset
    # elif self.instance.pk:
    #     self.fields['class_arm'].queryset = self.instance.studentrecord.class_arm_set.order_by(
    #         'class_arm')

    if 'studentrecord' in self.data:
        try:
            studentrecord_id = int(self.data.get('studentrecord'))
            self.fields['sex'].queryset = Gender.objects.filter(
                studentrecord_id=studentrecord_id).order_by('sex')
        except (ValueError, TypeError):
            pass  # invalid input from the client; ignore and fallback to empty City queryset
    elif self.instance.pk:
        self.fields['sex'].queryset = self.instance.studentrecord.sex_set.order_by(
            'sex')

    # if 'studentrecord' in self.data:
    #     try:
    #         studentrecord_id = int(self.data.get('studentrecord'))
    #         self.fields['program_type'].queryset = ProgramType.objects.filter(
    #             studentrecord_id=studentrecord_id).order_by('program_type')
    #     except (ValueError, TypeError):
    #         pass  # invalid input from the client; ignore and fallback to empty City queryset
    # elif self.instance.pk:
    #     self.fields['program_type'].queryset = self.instance.studentrecord.program_type_set.order_by(
    #         'program_type')


class Register(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control'}), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control'}), label='Confirm Password')

    class meta():
        model = User
        fields = ['username']
