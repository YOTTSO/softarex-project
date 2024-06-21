from django import forms


class UserForm(forms.ModelForm):
    login = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class PredictionForm(forms.Form):
    open_date = forms.CharField(max_length=12)
    city = forms.CharField(max_length=25)
    type = forms.CharField(max_length=20)
    break_point_1 = forms.IntegerField()
    break_point_2 = forms.IntegerField()
    break_point_3 = forms.IntegerField()
    break_point_4 = forms.IntegerField()
    break_point_5 = forms.IntegerField()
    break_point_6 = forms.IntegerField()
    break_point_7 = forms.IntegerField()
    break_point_8 = forms.IntegerField()
    break_point_9 = forms.IntegerField()
    break_point_10 = forms.IntegerField()
    break_point_11 = forms.IntegerField()
    break_point_12 = forms.IntegerField()