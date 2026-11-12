from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Review


class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "email")


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = (
            "review",
            "purchase",
            "purchase_date",
            "car_make",
            "car_model",
            "car_year",
        )
        widgets = {
            "review": forms.Textarea(attrs={"rows": 5}),
            "purchase_date": forms.DateInput(attrs={"type": "date"}),
            "car_year": forms.NumberInput(attrs={"min": 1886, "max": 2100}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("purchase") and not cleaned_data.get("purchase_date"):
            self.add_error("purchase_date", "Enter the purchase date.")
        return cleaned_data
