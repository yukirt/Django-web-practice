from django import forms
from . import models

class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ['height', 'male', 'website']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['height'].label = "身高（cm）"
        self.fields['male'].label = "是男生嗎？"
        self.fields['website'].label = "個人網站"

class LoginForm(forms.Form):
    COLORS = [
        ['紅', '紅'],
        ['黃', '黃'],
        ['綠', '綠'],
        ['紫', '紫'],
        ['藍', '藍'],
    ]
    user_name = forms.CharField(label='姓名', max_length=10)
    password = forms.CharField(label='密碼', widget=forms.PasswordInput())
    # user_color = forms.ChoiceField(label='幸運顏色', choices=COLORS)

class DateInput(forms.DateInput):
    input_type = 'date'

class DiaryForm(forms.ModelForm):
    
    class Meta:
        model = models.Diary
        fields = ['budget', 'weight', 'note', 'ddate']
        widgets = {
            'ddate': DateInput()
        }

    def __init__(self, *args, **kwargs):
        super(DiaryForm, self).__init__(*args, **kwargs)
        self.fields['budget'].label = '今日花費（元）'
        self.fields['weight'].label = '今日體重（kg）'
        self.fields['note'].label = '心情留言'
        self.fields['ddate'].label = '日期'
