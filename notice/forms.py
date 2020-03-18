from django import forms


class AckForm(forms.Form):
    acked = forms.BooleanField(label='我已阅读')
