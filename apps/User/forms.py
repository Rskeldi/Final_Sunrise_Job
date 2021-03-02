from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    def clean_password2(self):
        clean_data = self.cleaned_data
        if clean_data['password'] != clean_data['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return clean_data['password2']

    def save(self):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.create_activation_code()
        user.email_user()
        user.is_active = False
        user.save()
        return user

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class UserLoginForm(forms.Form):
    email = forms.CharField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')


class UserEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'postInpName', 'id': 'InpName'})
        self.fields['last_name'].widget.attrs.update({'class': 'postInpLast', 'id': 'InpLast'})

    class Meta:
        model = User
        fields = ('first_name', 'last_name')
