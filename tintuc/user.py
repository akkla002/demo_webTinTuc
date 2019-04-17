from tintuc.models import *
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class RegistrationFrom(forms.Form):
    name=forms.CharField(label='Tài khoản', max_length=255)
    email=forms.CharField(label='Email')
    password1=forms.CharField(label='Mật khẩu', widget=forms.PasswordInput())
    password2=forms.CharField(label='Nhập lại mật khẩu', widget=forms.PasswordInput())
    
    def clean_password2(self):
        if 'password1'in self.cleaned_data:
            password1=self.cleaned_data['password1']
            password2=self.cleaned_data['password2']
            if password1==password2 and password1:
                return password2
        raise forms.ValidationError("Mật khẩu không hợp lệ")

    def clean_username(self):
        name=self.cleaned_data['name']
        try:
            User.objects.get(name=name)
        except ObjectDoesNotExist:
            return name
        raise forms.ValidationError("Tài khoản đã tồn tại")