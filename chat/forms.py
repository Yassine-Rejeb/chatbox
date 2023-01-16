from django import forms

class updateForm(forms.Form):
    username = forms.CharField(max_length=100)
    new_password = forms.CharField(max_length=100)
    new_password2 = forms.CharField(max_length=100)
    current_password = forms.CharField(max_length=100)

    
