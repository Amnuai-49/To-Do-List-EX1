from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Task, Profile

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "category", "remind_at"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "remind_at": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        }
    def __init__(self, *a, user=None, **kw):
        super().__init__(*a, **kw)
        self.fields["remind_at"].input_formats = ["%Y-%m-%dT%H:%M"]
        if user: self.fields["category"].queryset = user.category_set.all()

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["telegram_chat_id"]
        widgets = {"telegram_chat_id": forms.TextInput(attrs={"class": "form-control"})}

class SignupForm(UserCreationForm):
    pass
