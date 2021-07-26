from django import forms


class AddUserOrderForm(forms.Form):
    course_id = forms.IntegerField(
        widget=forms.HiddenInput()
    )
