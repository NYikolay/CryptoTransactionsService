from django import forms

from .models import Network, ServiceAccount, Transaction


class ServiceAccountAdminForm(forms.ModelForm):

    class Meta:
        model = ServiceAccount
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        network = cleaned_data.get('network')
        cryptocurrency = cleaned_data.get('cryptocurrency').name
        valid_cryptocurrencies = network.currencies.values_list('name', flat=True)
        if cryptocurrency not in valid_cryptocurrencies:
            self.add_error('cryptocurrency', f'{network} has no such currency as {cryptocurrency}')


class TransactionForm(forms.ModelForm):
    sender_address = forms.ModelChoiceField(
        queryset=None,
        label=False,
        empty_label="Select Sender Address",
    )

    class Meta:
        model = Transaction
        fields = '__all__'
        widgets = {
            "sender": forms.HiddenInput(),
            "status": forms.HiddenInput(),
            "recipient_address": forms.TextInput(attrs={
                "placeholder": "Recipient address"
            }),
            "amount": forms.NumberInput(attrs={
                "placeholder": "Amount"
            })
        }
        labels = {
            "recipient_address": False,
            "amount": False,
        }

    def __init__(self, *args, **kwargs):
        sender_address_queryset = kwargs.pop('sender_address_queryset', None)
        super().__init__(*args, **kwargs)
        self.fields['sender_address'].queryset = sender_address_queryset

