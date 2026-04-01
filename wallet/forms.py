from django import forms
from .models import PaymentSource

class AddMoneyForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=1)
    source = forms.ModelChoiceField(queryset=PaymentSource.objects.none(), required=False)
    new_source_type = forms.ChoiceField(
        choices=[('', '-- Select --'), ('savings', 'Savings Account'), ('credit', 'Credit Card')],
        required=False
    )
    new_account_number = forms.CharField(max_length=20, required=False)
    new_label = forms.CharField(max_length=50, required=False)
    save_source = forms.BooleanField(required=False)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['source'].queryset = PaymentSource.objects.filter(user=user)