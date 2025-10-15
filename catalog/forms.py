# catalog/forms.py
from django import forms
from .models import Review

class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3, "placeholder": "Enter your shipping address"}),
        label="Shipping Address"
    )
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={"placeholder": "Phone number"}),
        label="Phone"
    )


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.NumberInput(attrs={"min": 1, "max": 5, "class": "form-control"}),
            "comment": forms.Textarea(attrs={"rows": 3, "placeholder": "Write your review...", "class": "form-control"}),
        }


class SearchForm(forms.Form):
    q = forms.CharField(
        label='Search',
        widget=forms.TextInput(attrs={'placeholder': 'Search products...', 'class': 'form-control'})
    )
