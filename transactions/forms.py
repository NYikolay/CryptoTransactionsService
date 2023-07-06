from django import forms

from .models import Network, ServiceAccount


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
