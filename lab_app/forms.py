from django import forms
from . models import BannerImage, PeopleCategory


class BannerImageForm(forms.ModelForm):
    class Meta:
        model = BannerImage
        fields = ['image']


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class PeopleCategoryForm(forms.ModelForm):
    class Meta:
        model = PeopleCategory
        fields = ['category']