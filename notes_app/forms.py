from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student, Reminder


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    reg_number = forms.CharField(max_length=50, required=True, label='Registration Number')
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Student.objects.create(
                user=user,
                reg_number=self.cleaned_data['reg_number'].upper(),
                gender=self.cleaned_data['gender']
            )
        return user


class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['unit', 'note', 'reminder_time', 'message']
        widgets = {
            'reminder_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'message': forms.Textarea(attrs={'rows': 3}),
        }
