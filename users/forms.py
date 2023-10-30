from django import forms

class PaymentMethodForm(forms.Form):
    payment_type = forms.ChoiceField(
        choices=(
            ('visa', 'Visa'),
            ('mastercard', 'Mastercard'),
            ('debit_card', 'Debit Card'),
        ),
        label='Payment Type',
    )
    card_number = forms.CharField(max_length=16, label='Card Number')
    cardholder_name = forms.CharField(max_length=255, label='Cardholder Name')
    expiration_month = forms.IntegerField(min_value=1, max_value=12, label='Expiration Month')
    expiration_year = forms.IntegerField(min_value=2023, label='Expiration Year')
    cvv = forms.IntegerField(min_value=100, label='CVV')

class RefundRequestForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea)