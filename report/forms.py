from django import forms
from django.core.exceptions import ValidationError

from bootstrap_datepicker_plus import DatePickerInput

from .models import Person, Record, Entry


class ProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['idnum'].disabled = True
        self.fields['name'].disabled = True
        self.fields['affiliation'].disabled = True

    class Meta:
        model = Person
        fields = ('name', 'idnum', 'affiliation', 'phone', 'phone2', 'remark')
        widgets = {
            'remark': forms.Textarea({'placeholder': '需要向学校反映的问题或意见'}),
        }


class RecordForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].disabled = True

    class Meta:
        model = Record
        fields = ('date', 'temperature', 'has_fever', 'has_cough', 'has_wornout', 'remark')
        widgets = {
            'temperature': forms.NumberInput({'placeholder': '如无不适可留空，单位℃，保留小数点后一位', 'autofocus': True}),
            'remark': forms.Textarea({'placeholder': '在此填写其他不适症状'}),
        }

    def clean(self):
        data = super().clean()
        if 'healthy' in self.data:
            if data['has_fever'] or data['has_cough'] or data['has_wornout']:
                raise ValidationError('无症状才能点击“一切正常！”按钮', 'invalid-state')
        return data

class EntryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['building'].queryset = self.fields['building'].queryset.order_by('-weight', 'name')

    class Meta:
        model = Entry
        fields = ('date', 'building', 'room', 'purpose')
        widgets = {
            'date': DatePickerInput(options={
                'format': 'YYYY/MM/DD',
                'locale': 'zh-CN',
            }),
        }
