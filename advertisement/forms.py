from django import forms
from .models import Advertisement, Response, Subscription


class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = [
            'category',
            'heading',
            'content',
        ]


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = [
            'text',
        ]




class SubscriptionForm(forms.Form):
    categories = forms.MultipleChoiceField(
        choices=Subscription.CATEGORY,
        widget=forms.CheckboxSelectMultiple,  # Позволяет выбрать несколько категорий
        label="Выберите категории для подписки"
    )